from src.data.db_conn import get_shopping_history, get_products_by_prod_cat
import numpy as np
from sklearn.cluster import KMeans

default_dialog_options = {
    "ok, removing":
        ["yes", "yep", "sure", "let's do it", "lets do it", "why not"],
    "if you say so":
        ["no", "nope", "abort", "cancel"]
}


def chat(case_tag, size, input):
    dialog_options = default_dialog_options
    if case_tag == "size":
        is_normal, usual_size = is_normal_size(size)
        if not is_normal:
            return "You usually buy products of different size. Are you sure you want to proceed with size {} " \
                   "instead of {} which you usually buy?".format(size, usual_size)
    elif case_tag == "refunded_stuff":
        return "We recently experienced a lot of returns for this product. Maybe you want to look for alternatives?"
    elif case_tag == "price":
        return "We noticed that you usually buy products from different price category. " \
               "Just checking if you want to continue."
    if input:
        for answer in dialog_options:
            lowercase = input.lower()

            if lowercase in dialog_options[answer]:
                return answer
    return None


def is_normal_size(size: float, demo_cus_name: str = "demo_customer", is_flex: bool = False):
    purchases = list(filter(lambda row: row[0] == demo_cus_name, get_shopping_history(demo_name="demo_1")))

    possible_sizes = set([purchase[4] for purchase in purchases])

    if is_flex:
        smaller_sizes = set([size - 0.5 for size in possible_sizes])
        larger_sizes = set([size + 0.5 for size in possible_sizes])

        possible_sizes = possible_sizes | smaller_sizes | larger_sizes

    return size in possible_sizes, possible_sizes.pop()


def is_abnormal_price(price: float, prod_cat: str, demo_cus_name: str = "demo_customer", is_flex: bool = False):
    products = get_products_by_prod_cat(demo_name="demo_1", prod_cat=prod_cat)
    product_prices = np.array([prod[3] for prod in products]).astype(float)

    purchases = list(filter(lambda row: row[0] == demo_cus_name, get_shopping_history(demo_name="demo_1")))
    historical_prices = np.array([purchase[5] for purchase in purchases])

    kmeans_data = np.dstack((np.zeros(product_prices.shape), product_prices))[0]

    kmeans = KMeans(n_clusters=3, random_state=0).fit(kmeans_data)

    cluster_centers = sorted(list(enumerate(kmeans.cluster_centers_[:, 1].tolist())), key=lambda o: o[1])
    sorted_cluster_ids = np.array(cluster_centers)[:, 0].astype(int)

    mappings = {
        sorted_cluster_ids[0]: "low",
        sorted_cluster_ids[1]: "mid",
        sorted_cluster_ids[2]: "high",
    }
    predicted_cluster_id = kmeans.predict([[0.0, price]])[0]
    print(price)
    print(predicted_cluster_id)

    return mappings[predicted_cluster_id]


if __name__ == '__main__':
    # print(is_abnormal_size(36))
    # print(is_abnormal_size(37))
    # print(is_abnormal_size(37, is_flex=True))
    # print(is_abnormal_size(35))
    # print(is_abnormal_size(35, is_flex=True))

    print(is_abnormal_price(50.50, "shoes"))
    print(is_abnormal_price(69.69, "shoes"))
    print(is_abnormal_price(21.21, "shoes"))
    print(is_abnormal_price(77.77, "shoes"))
