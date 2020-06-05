<%!
    import config.project
    import config.python
    import user.personal
    import os
%>

# *${config.project.project_name}* project by ${user.personal.personal_fullname}

![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![GitHub](https://img.shields.io/github/license/veltzer/${config.project.github_repo_name})
![PyPI](https://img.shields.io/pypi/v/${config.python.package_name})
![PyPI - Format](https://img.shields.io/pypi/format/${config.python.package_name})
[![Downloads](https://pepy.tech/badge/pytsv)](https://pepy.tech/project/${config.python.package_name})
[![Downloads](https://pepy.tech/badge/pytsv/month)](https://pepy.tech/project/${config.python.package_name}/month)
[![Downloads](https://pepy.tech/badge/pytsv/week)](https://pepy.tech/project/${config.python.package_name}/week)


${config.project.project_short_description}

project website: ${config.project.project_website}

% if os.path.isfile("snipplets/main.md.mako"):
<%include file="../snipplets/main.md.mako" />
% endif
