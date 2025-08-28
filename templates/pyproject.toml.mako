<%!
    import pydmt.helpers.misc
    import pydmt.helpers.project
    import pydmt.helpers.python
    import pydmt.helpers.urls
    import config.python
    import config.personal
    import config.project
    import config.version
    import config.platform
%>[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "${pydmt.helpers.project.get_name()}"
version = "${pydmt.helpers.misc.get_version_str()}"
requires-python = "${config.platform.python_requires}"
authors = [
	{ name = "${config.personal.fullname}", email = "${config.personal.email}" }
]
maintainers = [
	{ name = "${config.personal.fullname}", email = "${config.personal.email}" }
]
description = "${config.project.description_short}"
readme = "README.md"
% if hasattr(config.python, "python_requires"):
	requires-python="${config.python.python_requires}"
% endif
license = "${config.platform.license_type}"
keywords=${pydmt.helpers.python.array_indented(0, config.project.keywords)}
classifiers = ${pydmt.helpers.python.array_indented(0, config.platform.classifiers)}
% if hasattr(config.python, "install_requires"):
dependencies = ${pydmt.helpers.python.array_indented(0, config.python.install_requires)}
% endif

[project.urls]
"Homepage" = "${pydmt.helpers.urls.get_website_source()}"
"Bug Tracker" = "${pydmt.helpers.urls.get_website_source()}/issues"
"Documentation" = "${pydmt.helpers.urls.get_website()}"
"Download" = "https://pypi.org/project/${config.project.name}/"
"Repository" = "${pydmt.helpers.urls.get_website_source()}"

% if hasattr(config.python, "scripts"):
[project.scripts]
% for key, value in config.python.scripts.items():
${key} = "${value}"
% endfor
% endif

[tool.ruff]
line-length = 130

[tool.pytest.ini_options]
pythonpath = ["src"]

[tool.hatch.build.targets.wheel]
packages = ["src/${config.project.name}"]

[tool.hatch.build.targets.sdist]
include = [
    "src/${config.project.name}/",
    "README.md",
    "LICENSE",
    "pyproject.toml"
]
exclude = [
    ".gitignore",
    ".github/",
    "tests/",
    "docs/",
    "config/",
    "*.md",
]

[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true

[tool.hatch.envs.default]
installer = "uv"

[tool.uv.pip]
prerelease = "disallow"
