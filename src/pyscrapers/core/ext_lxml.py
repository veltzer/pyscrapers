"""
This module is s set of utilities for this entire project
"""


import lxml
import lxml.html
import lxml.etree


def setup_prefix():
    # register regular expressions with lxml
    # this means that we can use regular expression functions like 'match'
    # by specifying 're:match' in our xpath expressions
    ns = lxml.etree.FunctionNamespace("http://exslt.org/regular-expressions")
    ns.prefix = 're'


def get_html_dom_content(response):
    """
    Get the content from a request
    :param response:
    :return:
    """
    response.raise_for_status()
    str_content = response.content.decode()
    root = lxml.html.fromstring(str_content)
    return root


def get_element_as_bytes(element):
    """
    turn xml element from etree to bytes
    :param element:
    :return:
    """
    return lxml.etree.tostring(element, pretty_print=True)


def get_element_as_string(element):
    """
    turn xml element from etree to string
    :param element:
    :return:
    """
    return lxml.etree.tostring(element, pretty_print=True).decode()


def print_element(element):
    """
    print xml elements from etree
    :param element:
    :return:
    """
    print(get_element_as_string(element))
