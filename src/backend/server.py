import os

from bottle import route, run, static_file, get, post, request
from truckpad.bottle.cors import enable_cors

from src.backend.services import chat
from src.data.data_generator import gen_demo_1


@enable_cors
@route("/")
def index():
    return server_static("index.html")


@enable_cors
@post("/chat")
def handle_input():
    input = request.forms.get("input")
    case_tag = request.forms.get("case_tag")
    size = float(request.forms.get("size"))
    return chat(case_tag, size, input)


@enable_cors
@get("/usually-returned/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root="web/static/usually-returned")


if __name__ == '__main__':
    gen_demo_1()
    port = int(os.getenv("PORT"))
    run(host="0.0.0.0", port=port, debug=True)
