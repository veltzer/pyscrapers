<%!
    import config.version
    import config.project
%>""" version which can be consumed from within the module """
VERSION_STR = "${config.version.version_str}"
DESCRIPTION = "${config.project.project_short_description}"
APP_NAME = "${config.project.project_name}"
