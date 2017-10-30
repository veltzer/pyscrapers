#!/usr/bin/env python
import os
from pydmt.builders.mako import Mako
from pydmt.core.pydmt import PyDMT, BuildProcessStats

pydmt = PyDMT()
b = Mako(
    definitions_folders=['definitions', os.path.expanduser("~/.config/pydmt")],
    source="templates/README.rst.mako",
    target="README.rst",
)
pydmt.add_builder(b)
stats = BuildProcessStats()
pydmt.build_by_builder(b, stats=stats)
print(stats.fail)
print(stats.exceptions)
