def str_repeat(str, count):
    return str * count


def tab(count):
    return str_repeat("\t", count)


def space(count):
    return str_repeat(" ", count)


def tabspace(count):
    return str_repeat("    ", count)


def str_pad_left(s, length, pad_char):
    s = str(s)
    str_len = len(s)
    if length > str_len:
        diff = length - str_len
        s = (pad_char * diff) + s
    return s

def str_pad_right(s, length, pad_char):
    s = str(s)
    str_len = len(s)
    if length > str_len:
        diff = length - str_len
        s += pad_char * diff
    return s


def str_quote(str):
    return "\"" + str + "\"";

