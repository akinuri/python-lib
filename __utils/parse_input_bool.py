def parse_input_bool(input_value):
    yes_values = ["y", "yes", "1"]
    no_values  = ["n", "no", "0"]
    input_value = input_value.lower()
    if input_value in yes_values:
        return True
    elif input_value in no_values:
        return False
    return None