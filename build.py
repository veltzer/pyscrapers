#!/usr/bin/env python
from pydmt.builders.mako import Mako
from pydmt.core.pydmt import PyDMT, BuildProcessStats

pydmt = PyDMT()
b = Mako(
    definitions_folder='definitions',
    source="templates/README.rst.mako",
    target="README.rst",
)
pydmt.add_builder(b)
stats = BuildProcessStats()
pydmt.build_by_builder(b, stats=stats)
print(stats.fail)
print(stats.exceptions)
