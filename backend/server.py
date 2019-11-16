from bottle import route, run, static_file, get
from dotenv import load_dotenv


@route("/")
def index():
    return server_static("index.html")


@get("/usually-returned/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root="web/static/usually-returned")


if __name__ == '__main__':
    # TEMPLATE_PATH.append("../web/index_files")
    load_dotenv()
    run(host="localhost", port=8080, debug=True)
