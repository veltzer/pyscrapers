"""
dependencies for this project
"""


def populate(d):
    d.requirements3 = [
        'lxml',
        'requests',
        'browser-cookie3',
        'pylogconf',
    ]


def get_deps():
    return [
        __file__,  # myself
    ]
