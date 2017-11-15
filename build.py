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
pydmt.build_all()
