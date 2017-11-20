#!/usr/bin/env python

# noinspection PyUnresolvedReferences
import config
# noinspection PyUnresolvedReferences
import config.python
# noinspection PyUnresolvedReferences
import config.personal
# noinspection PyUnresolvedReferences
import config.project

from pydmt.builders.sphinx import Sphinx
from pydmt.core.pydmt import PyDMT
from pydmt.features.templating import Templating
import pylogconf

import pyscrapers.version
import pyscrapers.core.config

pylogconf.setup()
p = PyDMT()
f = Templating(data={
    "config": config,
    "version": pyscrapers.version,
    "own": pyscrapers.core.config,
})
f.setup(p)
b = Sphinx(package_name=config.python.project_name)
p.add_builder(b)
p.build_all()
