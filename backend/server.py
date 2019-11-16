from bottle import route, run, static_file, get, post, request
from dotenv import load_dotenv

from backend.services import chat


@route("/")
def index():
    return server_static("index.html")


@post("/chat")
def handle_input():
    input = request.forms.get("input")
    case_tag = request.forms.get("case_tag")
    return chat(case_tag, input)


@get("/usually-returned/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root="web/static/usually-returned")


if __name__ == '__main__':
    load_dotenv()
    run(host="localhost", port=8080, debug=True)
