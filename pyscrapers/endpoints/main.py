"""
main entry point to the program
"""


import pylogconf.core
from pytconf import register_main, config_arg_parse_and_launch 

from pyscrapers.endpoints.group_default import register_group_default


def register_all_groups():
    """
    registers all groups of operations with pytconf
    """
    register_group_default()


@register_main()
def main():
    """
    pyscapers will help you download stuff from the web
    """
    pylogconf.core.setup()
    register_all_groups()
    config_arg_parse_and_launch(app_name="pyscrapers")


if __name__ == '__main__':
    main()
