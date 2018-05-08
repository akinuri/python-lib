def str_repeat(str, count):
    return str * count

def tab(count):
    return str_repeat("\t", count)

def space(count):
    return str_repeat(" ", count)

def tabspace(count):
    return str_repeat("    ", count)

def str_pad_right(str, length, pad_char):
    str_len = len(str)
    if length > str_len:
        diff = length - str_len
        str += pad_char * diff
    return str

