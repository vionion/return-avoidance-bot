import os

from bottle import route, run, static_file, get, post, request
from truckpad.bottle.cors import enable_cors

from src.backend.services import chat
from src.data.data_generator import gen_demo_1


@enable_cors
@route("/")
def index():
    return usually_returned("index.html")


@enable_cors
@route("/2")
def index():
    return wrong_size("index.html")


@enable_cors
@post("/chat")
def handle_input():
    input = request.forms.get("input")
    case_tag = request.forms.get("case_tag")
    size = float(request.forms.get("size"))
    return chat(case_tag, size, input)


@enable_cors
@get("/usually-returned/<filepath:path>")
def usually_returned(filepath):
    return static_file(filepath, root="web/static/usually-returned")


@enable_cors
@get("/wrong-size/<filepath:path>")
def wrong_size(filepath):
    return static_file(filepath, root="web/static/wrong-size")


if __name__ == '__main__':
    gen_demo_1()
    port = int(os.getenv("PORT"))
    run(host="0.0.0.0", port=port, debug=True)
