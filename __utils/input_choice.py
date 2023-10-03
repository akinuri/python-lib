def input_choice(text, options=[], keepAsking=True, default=None):
    user_input = input(text)
    if user_input not in options:
        if default is None and keepAsking:
            print("Input does not match the options.")
            user_input = input_choice(text, options, keepAsking, default)
        else:
            user_input = default
            print("Using the default value: %s" % default)
    return user_input