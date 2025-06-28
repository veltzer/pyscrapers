<%!
    import pydmt.helpers.misc
    import pydmt.helpers.project
    import config.version
    import config.project
%>""" version which can be consumed from within the module """
VERSION_STR = "${pydmt.helpers.misc.get_version_str()}"
DESCRIPTION = "${config.project.description_short}"
APP_NAME = "${pydmt.helpers.project.get_name()}"
LOGGER_NAME = "${pydmt.helpers.project.get_name()}"
