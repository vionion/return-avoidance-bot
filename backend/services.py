dialog_options = {
    "ok, removing":
        ["yes", "yep", "sure", "let's do it", "lets do it", "why not"],
    "if you say so":
        ["no", "nope", "abort", "cancel"]
}


def chat(case_tag, size, input):
    lowercase = input.lower()
    for answer in dialog_options:
        if lowercase in dialog_options[answer]:
            return answer
