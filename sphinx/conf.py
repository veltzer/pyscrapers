extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
]
import datetime
import importlib.metadata
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

# The rendered HTML depends on the exact versions of sphinx and its rendering
# stack: building with any other version silently rewrites every page of the
# published docs/ tree. Refuse to build unless the running toolchain matches
# uv.lock, so a shell with the wrong environment active fails loudly instead
# of producing different output.
with open(os.path.join(_here, "..", "uv.lock"), "rb") as _f:
    _locked = {p["name"]: p["version"] for p in tomllib.load(_f)["package"]}
for _pkg in ("sphinx", "docutils", "alabaster"):
    _running = importlib.metadata.version(_pkg)
    if _running != _locked[_pkg]:
        raise RuntimeError(
            f"{_pkg} {_running} does not match uv.lock ({_locked[_pkg]}); "
            "the docs would render differently - activate this repository's venv"
        )

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
