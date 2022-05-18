<%!
    import pydmt.helpers.misc
    import pydmt.helpers.signature
    import config.project
    import config.python
    import user.personal
    import glob
    import yaml
%># *${config.project.name}* project by ${user.personal.personal_fullname}

project website: ${config.project.website}

author: ${user.personal.personal_fullname}

version: ${pydmt.helpers.misc.get_version_str()}

![PyPI - Status](https://img.shields.io/pypi/status/${config.python.package_name})
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/${config.python.package_name})
![PyPI - License](https://img.shields.io/pypi/l/${config.python.package_name})
![PyPI - Package Name](https://img.shields.io/pypi/v/${config.python.package_name})
![PyPI - Format](https://img.shields.io/pypi/format/${config.python.package_name})

![PyPI - Downloads](https://img.shields.io/pypi/dd/${config.python.package_name})
![PyPI - Downloads](https://img.shields.io/pypi/dw/${config.python.package_name})
![PyPI - Downloads](https://img.shields.io/pypi/dm/${config.python.package_name})

![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
% if hasattr(config.project, "codacy_id"):
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/${config.project.codacy_id})](https://www.codacy.com/app/jarrekk/imgkit?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=${config.project.github_username}/${config.python.package_name}&amp;utm_campaign=Badge_Grade)
% endif
<%doc>
![Downloads](https://pepy.tech/badge/${config.python.package_name})
![Downloads](https://pepy.tech/badge/${config.python.package_name}/month)
![Downloads](https://pepy.tech/badge/${config.python.package_name}/week)
[![Known Vulnerabilities](https://snyk.io/test/github/${config.project.github_username}/${config.project.github_repo_name}/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/${config.project.github_username}/${config.project.github_repo_name}?targetFile=requirements.txt)</%doc>
<%
	action_files = glob.glob('.github/workflows/*.yml')
	for action_file in action_files:
		with open(action_file, 'r') as stream:
			action_name=yaml.safe_load(stream)["name"]
			context.write(f"![{action_name}](https://github.com/{config.project.github_username}/{config.project.name}/workflows/{action_name}/badge.svg)")
%>
${config.project.description_short}

project website: ${config.project.website}

chat with me at [![gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/veltzer/mark.veltzer)

<%include file="../snipplets/main.md.mako" />

	${user.personal.personal_origin}, ${pydmt.helpers.signature.get_copyright_years_long()}
