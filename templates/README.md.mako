<%!
    import config.project
    import config.python
    import user.personal
    import glob
    import yaml
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
<%doc>
![Downloads](https://pepy.tech/badge/${config.python.package_name})
![Downloads](https://pepy.tech/badge/${config.python.package_name}/month)
![Downloads](https://pepy.tech/badge/${config.python.package_name}/week)
[![Known Vulnerabilities](https://snyk.io/test/github/${config.project.project_github_username}/${config.project.github_repo_name}/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/${config.project.project_github_username}/${config.project.github_repo_name}?targetFile=requirements.txt)</%doc>
<%
	actions = glob.glob('.github/workflows/*.yml')
	names = []
	for action in actions:
		with open(action, 'r') as stream:
			names.append(yaml.safe_load(stream)["name"])
%>
% if names:
Actions

	% for name in names:
![${name}](https://github.com/veltzer/${config.project.project_name}/workflows/${name}/badge.svg)
	% endfor
% endif

${config.project.project_short_description}

project website: ${config.project.project_website}

chat with me at [![gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/veltzer/mark.veltzer)

<%include file="../snipplets/main.md.mako" />
