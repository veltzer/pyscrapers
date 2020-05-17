from typing import List

import os


def array_indented(level: int, my_list: List[str], quote_char='\'', comma_after=False) -> str:
    """
    return an array indented according to indent level
    :param level:
    :param my_list:
    :param quote_char:
    :param comma_after:
    :return:
    """
    out = "[\n"
    for x in my_list:
        out += (((level+1) * 4) * " ") + '{}{}{}'.format(quote_char, x, quote_char) + ",\n"
    out += ((level * 4) * " ") + "]"
    if comma_after:
        out += ","
    return out


def find_packages(path: str) -> List[str]:
    """
    A better version of find_packages than what setuptools offers
    :param path:
    :return:
    """
    for root, _dir, files in os.walk(path):
        if '__init__.py' in files:
            yield root.replace("/", ".")
