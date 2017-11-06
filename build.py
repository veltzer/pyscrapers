#!/usr/bin/env python

from pydmt.core.pydmt import PyDMT
from pydmt.features.templating import Templating
import pylogconf

pylogconf.setup()
pydmt = PyDMT()
f = Templating()
f.setup(pydmt)
pydmt.build_all()
