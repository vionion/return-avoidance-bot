default_dialog_options = {
    "ok, removing":
        ["yes", "yep", "sure", "let's do it", "lets do it", "why not"],
    "if you say so":
        ["no", "nope", "abort", "cancel"]
}


def chat(case_tag, size, input):
    lowercase = input.lower()
    dialog_options = default_dialog_options
    if case_tag == "size":
        return "You usually buy products of different size. Are you sure you want to with size {}?".format(size)
    elif case_tag == "refunded_stuff":
        return "We recently experienced a lot of returns for this product. Maybe you want to look for alternatives?"
    elif case_tag == "price":
        return "We noticed that you usually buy products from different price category. Just checking if you want to continue."
    for answer in dialog_options:
        if lowercase in dialog_options[answer]:
            return answer
