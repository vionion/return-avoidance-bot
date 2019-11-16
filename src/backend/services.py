from src.data.db_conn import _get_shopping_history

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
    rows = _get_shopping_history(demo_name="demo_1")

    purchases = list(filter(lambda row: row[0] == demo_cus_name, rows))

    possible_sizes = set([purchase[4] for purchase in purchases])

    if is_flex:
        smaller_sizes = set([size - 0.5 for size in possible_sizes])
        larger_sizes = set([size + 0.5 for size in possible_sizes])

        possible_sizes = possible_sizes | smaller_sizes | larger_sizes

    return size in possible_sizes, possible_sizes.pop()


if __name__ == '__main__':
    print(is_normal_size(36))
    print(is_normal_size(37))
    print(is_normal_size(37, is_flex=True))
    print(is_normal_size(35))
    print(is_normal_size(35, is_flex=True))
