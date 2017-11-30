from typing import List


def array_indented(level: int, l: List[str], quote_char='"', comma_after=False) -> str:
    out = "[\n"
    for x in l:
        out += (((level+1) * 4) * " ") + '{}{}{}'.format(quote_char, x, quote_char) + ",\n"
    out += ((level * 4) * " ") + "]"
    if comma_after:
        out += ","
    return out
