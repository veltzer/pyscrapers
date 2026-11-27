"""
This module is s set of utilities for this entire project
"""


from typing import TYPE_CHECKING, Any

import lxml
import lxml.etree
import lxml.html

if TYPE_CHECKING:
    import requests


def setup_prefix() -> None:
    # register regular expressions with lxml
    # this means that we can use regular expression functions like "match"
    # by specifying "re:match" in our xpath expressions
    ns = lxml.etree.FunctionNamespace("http://exslt.org/regular-expressions")
    ns.prefix = "re"


def get_html_dom_content(response: requests.Response) -> lxml.html.HtmlElement:
    """
    Get the content from a request
    :param response:
    :return:
    """
    response.raise_for_status()
    str_content = response.content.decode()
    return lxml.html.fromstring(str_content)


def xpath_elements(element: lxml.html.HtmlElement, expression: str) -> list[lxml.html.HtmlElement]:
    """
    Run an xpath expression that selects elements and return them as a typed list
    (lxml types the raw result of xpath() as a union of everything it can return)
    """
    result = element.xpath(expression)
    assert isinstance(result, list)
    return [x for x in result if isinstance(x, lxml.html.HtmlElement)]


def get_element_as_bytes(element: Any) -> bytes:
    """
    turn xml element from etree to bytes
    :param element:
    :return:
    """
    return lxml.etree.tostring(element, pretty_print=True)


def get_element_as_string(element: Any) -> str:
    """
    turn xml element from etree to string
    :param element:
    :return:
    """
    return lxml.etree.tostring(element, pretty_print=True).decode()


def print_element(element: Any) -> None:
    """
    print xml elements from etree
    :param element:
    :return:
    """
    print(get_element_as_string(element))
