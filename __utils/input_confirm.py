from __utils.parse_input_bool import parse_input_bool

def input_confirm(text):
    confirm = input(text)
    confirm = parse_input_bool(confirm)
    if confirm is None:
        print("")
        print("Please enter a valid input: %s" % ", ".join(["y", "yes", "1", "n", "no", "0"]))
        print("")
        confirm = input_confirm(text)
    return confirm