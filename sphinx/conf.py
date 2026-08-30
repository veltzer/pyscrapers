extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
]
import datetime
import os
import sys
import tomllib

# Add the projects "src" directory to the Python path.
# This allows Sphinx to find and import your package.
sys.path.insert(0, os.path.abspath("../src"))
sys.path.insert(0, os.path.abspath(".."))

# Treat all warnings as errors.
# This can also be set by passing the -W flag to the sphinx-build command.
warning_is_error = True

# Enable "nit-picky mode". This will issue warnings for all missing
# cross-references (e.g., a link to a class that doesnt exist).
# nitpicky = True

# This file is byte-identical in every repository: everything repo-specific
# (project name, version, author) is read at build time from pyproject.toml.
_here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_here, "..", "pyproject.toml"), "rb") as _f:
    _meta = tomllib.load(_f)["project"]

project = _meta["name"]
author = _meta["authors"][0]["name"]
version = _meta["version"]
release = version
project_copyright = f"{datetime.date.today().year} {author}"

html_theme_options = {
        "show_powered_by": False,
}
# allow us to use |project| in our snippets and rst files
rst_epilog = f"""
.. |project| replace:: {project}
"""
# title without a version
html_title = "%s Documentation" % project
# This is the default
# html_title = "%s %s Documentation" % (project, version)
