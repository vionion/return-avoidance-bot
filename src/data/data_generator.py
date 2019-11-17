from datetime import datetime
from sqlite3 import Connection

import numpy as np
from numpy.random import choice

from src.data.db_conn import _open_db_demo, PRODUCT_DATA_TABLE_NAME, RETURNS_TABLE_NAME, PURCHASES_TABLE_NAME

PROD_CATS = ["hobbies", "shoes", "clothes", "food"]

_PRODUCT_DATA_SQL = ("CREATE TABLE IF NOT EXISTS {} ("
                     "prod_name TEXT PRIMARY KEY,"
                     "prod_cat TEXT , "
                     "prod_sizes TEXT , "
                     "prod_price TEXT"
                     ")").format(PRODUCT_DATA_TABLE_NAME)

_RETURNS_SQL = ("CREATE TABLE IF NOT EXISTS {} ("
                "cus_name TEXT ,"
                "prod_name TEXT , "
                "return_timestamp INTEGER , "
                "prod_cat TEXT , "
                "prod_size FLOAT , "
                "prod_price FLOAT , "
                "PRIMARY KEY (cus_name, prod_name, return_timestamp)"
                ")").format(RETURNS_TABLE_NAME)

_PURCHASES_SQL = ("CREATE TABLE IF NOT EXISTS {} ("
                  "cus_name TEXT ,"
                  "prod_name TEXT , "
                  "purchase_timestamp INTEGER , "
                  "prod_cat TEXT , "
                  "prod_size FLOAT , "
                  "prod_price FLOAT , "
                  "PRIMARY KEY (cus_name, prod_name, purchase_timestamp)"
                  ")").format(PURCHASES_TABLE_NAME)

PROD_PRICE_CLUSTER_SEEDS = [0.25, 0.5, 0.75]
MAX_PROD_PRICE = 100.00


def _gen_prod_data(conn: Connection):
    # recreate table
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS {}".format(PRODUCT_DATA_TABLE_NAME))
    cursor.execute(_PRODUCT_DATA_SQL)
    conn.commit()

    # generate and insert random data
    for prod_cat in PROD_CATS:
        prod_count = 0
        for price_seed in PROD_PRICE_CLUSTER_SEEDS:
            prod_prices = np.random.logistic(
                loc=price_seed,
                scale=2 / MAX_PROD_PRICE,
                size=10 if price_seed != 0.5 else 20
            ) * MAX_PROD_PRICE

            prod_prices = prod_prices[prod_prices > MAX_PROD_PRICE * 0.1]
            prod_prices = prod_prices[prod_prices < MAX_PROD_PRICE * 0.9]

            for idx, prod_price in enumerate(prod_prices):
                prod_name = "{prod_cat}_{prod_idx}".format(
                    prod_cat=prod_cat,
                    prod_idx=prod_count + idx)

                # print(prod_name)

                if prod_cat in ["shoes", "clothes"]:
                    prod_sizes = np.linspace(30, 45, num=(45 - 30) * 2 + 1)
                else:
                    prod_sizes = [0, 1]

                cursor.execute(
                    "INSERT INTO {} (prod_name, prod_cat, prod_sizes, prod_price) "
                    "VALUES (?, ?, ?, ?)"
                    "".format(PRODUCT_DATA_TABLE_NAME),
                    (prod_name, prod_cat, str(prod_sizes), round(prod_price, 2)))

                conn.commit()

            prod_count += len(prod_prices)

            # plt.hist(prod_prices, bins=50)

    # cursor.execute("SELECT * FROM {}".format(_PRODUCT_DATA_TABLE_NAME))
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row)
    # plt.show()


def _gen_purchase_data(conn: Connection):
    # recreate table
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS {}".format(PURCHASES_TABLE_NAME))
    cursor.execute(_PURCHASES_SQL)
    conn.commit()

    demo_cus_name = "demo_customer"
    demo_prod_size = 7
    demo_prod_cat = "shoes"

    date_strs = [
        "11/01/2019 16:07:31",
        "25/01/2019 19:20:42",
        "06/04/2019 15:23:54",
        "05/05/2019 11:43:12",
        "11/05/2019 19:39:22",
        "17/05/2019 10:15:55",
        "13/06/2019 14:36:47",
        "22/07/2019 09:13:32",
        "07/09/2019 18:40:12",
        "30/09/2019 00:48:07"
    ]

    cursor.execute("SELECT prod_name, prod_cat, prod_sizes, prod_price FROM {} "
                   "WHERE prod_cat = ?"
                   "ORDER BY prod_price ASC "
                   "LIMIT ?"
                   "".format(PRODUCT_DATA_TABLE_NAME),
                   (demo_prod_cat, len(date_strs)))
    cheap_shoes = cursor.fetchall()

    for idx, date_str in enumerate(date_strs):
        date_time_obj = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
        purchase_timestamp = int(date_time_obj.timestamp())

        prod_name, _, _, prod_price = cheap_shoes[idx]

        cursor.execute(
            "INSERT INTO {} (cus_name, prod_name, purchase_timestamp, prod_cat, prod_size, prod_price) "
            "VALUES (?, ?, ?, ?, ?, ?)"
            "".format(PURCHASES_TABLE_NAME),
            (demo_cus_name, prod_name, purchase_timestamp, demo_prod_cat,
             demo_prod_size,
             prod_price))

        conn.commit()

    # cursor.execute("SELECT * FROM {}".format(_PURCHASES_TABLE_NAME))
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row)


def gen_demo_1():
    conn = _open_db_demo("demo_1")
    _gen_prod_data(conn)
    _gen_purchase_data(conn)


if __name__ == "__main__":
    gen_demo_1()
