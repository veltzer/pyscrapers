<%!
    import config.project
    import config.python
    import user.personal
    import config.version
    import os
    line = '=' * (len(config.project.project_name)+2)
%>${line}
*${config.project.project_name}*
${line}

.. image:: https://img.shields.io/pypi/v/${config.python.package_name}

.. image:: https://img.shields.io/github/license/veltzer/${config.project.project_name}

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg

project website: ${config.project.project_website}

author: ${user.personal.personal_fullname}

version: ${config.version.version_str}

<%include file="../snipplets/main.rst.mako" />
