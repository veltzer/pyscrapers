<%!
    import pydmt.helpers.misc
    import pydmt.helpers.signature
    import pydmt.helpers.project
    import pydmt.helpers.python
    import pydmt.helpers.urls
    import config.project
    import config.personal
    import glob
    import yaml
    import os
%># *${pydmt.helpers.project.get_name()}* project by ${config.personal.fullname}

description: ${config.project.description_short}

project website: ${pydmt.helpers.urls.get_website()}

author: ${config.personal.fullname}

version: ${pydmt.helpers.misc.get_version_str()}

![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

${"##"} github

![License](https://img.shields.io/github/license/veltzer/pytconf)

${"##"} build

<%
	action_files = glob.glob('.github/workflows/*.yml')
	for action_file in action_files:
		with open(action_file, 'r') as stream:
			action_name=yaml.safe_load(stream)["name"]
			context.write(f"![{action_name}](https://github.com/{config.personal.github_username}/{pydmt.helpers.project.get_name()}/workflows/{action_name}/badge.svg)")
%>

${"##"} pypi

![PyPI - Status](https://img.shields.io/pypi/status/${pydmt.helpers.python.get_package_name()})
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/${pydmt.helpers.python.get_package_name()})
![PyPI - License](https://img.shields.io/pypi/l/${pydmt.helpers.python.get_package_name()})
![PyPI - Package Name](https://img.shields.io/pypi/v/${pydmt.helpers.python.get_package_name()})
![PyPI - Format](https://img.shields.io/pypi/format/${pydmt.helpers.python.get_package_name()})

${"##"} pypi download

![PyPI - Downloads](https://img.shields.io/pypi/dd/${pydmt.helpers.python.get_package_name()})
![PyPI - Downloads](https://img.shields.io/pypi/dw/${pydmt.helpers.python.get_package_name()})
![PyPI - Downloads](https://img.shields.io/pypi/dm/${pydmt.helpers.python.get_package_name()})
<%doc>
![Downloads](https://pepy.tech/badge/${pydmt.helpers.python.get_package_name()})
![Downloads](https://pepy.tech/badge/${pydmt.helpers.python.get_package_name()}/week)
![Downloads](https://pepy.tech/badge/${pydmt.helpers.python.get_package_name()}/month)
</%doc>
% if hasattr(config.project, "codacy_id"):
${"##"} codacy stuff 

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/${config.project.codacy_id})](https://www.codacy.com/app/jarrekk/imgkit?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=${config.personal.github_username}/${pydmt.helpers.python.get_package_name()}&amp;utm_campaign=Badge_Grade)
% endif

% if os.path.isfile("../snipplets/main.md.mako"):
<%include file="../snipplets/main.md.mako" />
% endif

${"##"} contact me
[mailto](mailto:${config.personal.email})
![gitter](https://img.shields.io/gitter/room/veltzer/mark.veltzer)
![discord](https://img.shields.io/discord/719336281624281119)
![discord](https://img.shields.io/discord/719336282194444302)

${config.personal.fullname}, Copyright © ${pydmt.helpers.signature.get_copyright_years_long()}
