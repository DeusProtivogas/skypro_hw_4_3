import os

from flask import Flask, request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def exec_commands(query, file):
    cmds = list( map( lambda v: v.strip(), query.split('|')) )
    res = map( lambda v: v.strip(), file)

    for cmnd in cmds:
        words = cmnd.split(':')

        print(words)

        if words[0] == "filter":
            res = filter( lambda v, val=words[1]: val in v, res)
        elif words[0] == "map":
            res = map( lambda v, val=int(words[1]): v.split(' ')[val], res)
        elif words[0] == "sort":
            res = sorted( res, reverse= words[1] == "desc" )
        elif words[0] == "limit":
            res = list(res)[:int(words[1])]
        elif words[0] == "unique":
            res = set(res)
        else:
            return BadRequest(description=f"Command {'|'.join(words)} not found")

    return res

@app.route("/perform_query")
def perform_query():
    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    # вернуть пользователю сформированный результат

    try:
        query = request.args["query"]
        file_name = request.args["file_name"]
    except KeyError:
        raise BadRequest

    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        return BadRequest(description=f"File {file_name} not found")


    with open(file_path) as f:
        res = "\n".join( exec_commands(query, f) )
        print(res)

    return app.response_class('', content_type="text/plain")


app.run()