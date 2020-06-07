<%!
    import config.project
    import config.python
    import user.personal
    import os
%>

# *${config.project.project_name}* project by ${user.personal.personal_fullname}

![PyPI - Status](https://img.shields.io/pypi/status/${config.python.package_name})
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/${config.python.package_name})
![PyPI - License](https://img.shields.io/pypi/l/${config.python.package_name})
![PyPI - Package Name](https://img.shields.io/pypi/v/${config.python.package_name})
![PyPI - Format](https://img.shields.io/pypi/format/${config.python.package_name})

![PyPI - Downloads](https://img.shields.io/pypi/dd/${config.python.package_name})
![PyPI - Downloads](https://img.shields.io/pypi/dw/${config.python.package_name})
![PyPI - Downloads](https://img.shields.io/pypi/dm/${config.python.package_name})

![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Downloads](https://pepy.tech/badge/${config.python.package_name})
![Downloads](https://pepy.tech/badge/${config.python.package_name}/month)
![Downloads](https://pepy.tech/badge/${config.python.package_name}/week)

${config.project.project_short_description}

project website: ${config.project.project_website}

% if os.path.isfile("snipplets/main.md.mako"):
<%include file="../snipplets/main.md.mako" />
% endif
