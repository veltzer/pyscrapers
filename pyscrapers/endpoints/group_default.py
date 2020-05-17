"""
The default group of operations that pyscrapers has
"""

from pytconf.config import register_endpoint, register_function_group

import pyscrapers.version

GROUP_NAME_DEFAULT = "default"
GROUP_DESCRIPTION_DEFAULT = "all pyscapers commands"


def register_group_default():
    """
    register the name and description of this group
    """
    register_function_group(
        function_group_name=GROUP_NAME_DEFAULT,
        function_group_description=GROUP_DESCRIPTION_DEFAULT,
    )


@register_endpoint(
    configs=[],
    suggest_configs=[],
    group=GROUP_NAME_DEFAULT,
)
def version() -> None:
    """
    Print version
    """
    print(pyscrapers.version.VERSION_STR)
