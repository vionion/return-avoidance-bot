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


def _get_shopping_history(demo_name: str):
    conn = _open_db_demo(demo_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM {}".format(PURCHASES_TABLE_NAME))
    rows = cursor.fetchall()

    return rows


def is_abnormal_size(size: float, demo_cus_name: str = "demo_customer", is_flex: bool = False):
    rows = _get_shopping_history(demo_name="demo_1")

    purchases = list(filter(lambda row: row[0] == demo_cus_name, rows))

    possible_sizes = set([purchase[4] for purchase in purchases])

    if is_flex:
        smaller_sizes = set([size - 0.5 for size in possible_sizes])
        larger_sizes = set([size + 0.5 for size in possible_sizes])

        possible_sizes = possible_sizes | smaller_sizes | larger_sizes

    return size in possible_sizes


if __name__ == '__main__':
    print(is_abnormal_size(36))
    print(is_abnormal_size(37))
    print(is_abnormal_size(37, is_flex=True))
    print(is_abnormal_size(35))
    print(is_abnormal_size(35, is_flex=True))
