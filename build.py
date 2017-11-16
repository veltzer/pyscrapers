#!/usr/bin/env python

from pydmt.builders.sphinx import Sphinx
from pydmt.core.pydmt import PyDMT
from pydmt.features.templating import Templating
import pylogconf
import definitions.project

pylogconf.setup()
pydmt = PyDMT()
f = Templating()
f.setup(pydmt)
b = Sphinx(package_name=definitions.project.project_name)
pydmt.add_builder(b)
stats = pydmt.build_all()
# print(stats.builder_fail[0][1])
