#!/usr/bin/env python

from pydmt.core import PyDMT
from pydmt.builders import Mako

pydmt = PyDMT()
pydmt.add(Mako(
    source="templates/README.md.mako",
    target="README.md.mako",
    defs=['defs/project.py'],
))

pydmt.build()
