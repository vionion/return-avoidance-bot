from bottle import route, run, TEMPLATE_PATH, view
from dotenv import load_dotenv

from backend.services import get_some_stuff


@route("/")
@view("index")
def index():
    return dict(logs=get_some_stuff())


if __name__ == '__main__':
    TEMPLATE_PATH.append("../web/templates")
    load_dotenv()
    run(host="localhost", port=8080, debug=True)
