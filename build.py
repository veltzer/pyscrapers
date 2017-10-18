#!/usr/bin/env python

from pydmt.core import PyDMT
from pydmt.builders import Mako

pydmt = PyDMT()
pydmt.add(Mako(
    source="templartmpl/README.md.mako",
    target="README.md.mako",
    parameters=
))

pydmt.build()
