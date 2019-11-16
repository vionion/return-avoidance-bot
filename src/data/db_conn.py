from os.path import abspath, join, pardir
from sqlite3 import connect

PRODUCT_DATA_TABLE_NAME = "prod_data"

PURCHASES_TABLE_NAME = "purchases"

RETURNS_TABLE_NAME = "returns"


def _open_db_demo(demo_name: str):
    db_name = "{}.db".format(demo_name)
    db_path = abspath(join(join(abspath(__file__), pardir), db_name))

    conn = connect(db_path)
    return conn


def get_shopping_history(demo_name: str):
    conn = _open_db_demo(demo_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM {}".format(PURCHASES_TABLE_NAME))
    rows = cursor.fetchall()

    return rows


def get_products_by_prod_cat(demo_name: str, prod_cat: str):
    conn = _open_db_demo(demo_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM {} "
                   "WHERE prod_cat = ?"
                   "".format(PRODUCT_DATA_TABLE_NAME),
                   (prod_cat,))
    rows = cursor.fetchall()

    return rows
