<%!
    import pydmt.helpers.misc
    import pydmt.helpers.signature
    import pydmt.helpers.project
    import pydmt.helpers.python
    import pydmt.helpers.urls
    import config.project
    import config.python
    import config.personal
    import config.version
    import os
    line = '=' * (len(pydmt.helpers.project.get_name())+2)
%>${line}
*${pydmt.helpers.project.get_name()}*
${line}

.. image:: https://img.shields.io/pypi/v/${pydmt.helpers.python.get_package_name()}

.. image:: https://img.shields.io/github/license/veltzer/${pydmt.helpers.project.get_name()}

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg

project website: ${pydmt.helpers.urls.get_website()}

author: ${config.personal.fullname}

version: ${pydmt.helpers.misc.get_version_str()}

% if os.path.isfile("../snipplets/main.md.mako"):
<%include file="../snipplets/main.rst.mako" />
% endif
	${config.personal.origin}, Copyright © ${pydmt.helpers.signature.get_copyright_years_long()}
