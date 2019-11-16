import os

from bottle import route, run, static_file, get, post, request

from data.data_generator import gen_demo_1

from backend.services import chat


@route("/")
def index():
    return server_static("index.html")


@post("/chat")
def handle_input():
    input = request.forms.get("input")
    case_tag = request.forms.get("case_tag")
    size = request.forms.get("size")
    return chat(case_tag, size, input)


@get("/usually-returned/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root="web/static/usually-returned")


if __name__ == '__main__':
    gen_demo_1()
    port = int(os.getenv("PORT"))
    run(host="0.0.0.0", port=port, debug=True)
