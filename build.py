#!/usr/bin/env python

from pydmt.core import PyDMT
from pydmt.builders import MakoBuilder

pydmt = PyDMT()
pydmt.add(MakoBuilder(
    sources=["templartmpl/README.md.mako"],
    targets=["README.md.mako"],
))

pydmt.build()
