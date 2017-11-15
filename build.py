#!/usr/bin/env python

from pydmt.builders.sphinx import Sphinx
from pydmt.core.pydmt import PyDMT
from pydmt.features.templating import Templating
import pylogconf

pylogconf.setup()
pydmt = PyDMT()
f = Templating()
f.setup(pydmt)
b = Sphinx(package_name="pyscrapers")
pydmt.add_builder(b)
stats = pydmt.build_all()
# print(stats.builder_fail[0][1])
