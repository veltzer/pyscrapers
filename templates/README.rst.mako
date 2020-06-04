<%!
    import config.project
    import user.personal
    import config.version
    import os
    line = '=' * (len(config.project.project_name)+2)
%>${line}
*${config.project.project_name}*
${line}

.. image:: https://img.shields.io/github/license/veltzer/pydmt   :alt: GitHub

![build](https://github.com/veltzer/${config.project.github_repo_name}/workflows/build/badge.svg)

project website: ${config.project.project_website}

author: ${user.personal.personal_fullname}

version: ${config.version.version_str}

% if os.path.isfile("snipplets/main.rst.mako"):
<%include file="../snipplets/main.rst.mako" />
% endif
