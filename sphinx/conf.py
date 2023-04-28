extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.coverage',
              'sphinx.ext.viewcode']

import config.project
project = config.project.name
import config.personal
author = config.personal.fullname
# FIXME
project_copyright = author
import config.version
version = ".".join(str(x) for x in config.version.tup)
release = ".".join(str(x) for x in config.version.tup)

html_theme_options = {
        "show_powered_by": "false",
}
rst_epilog = f'''
.. |project| replace:: {project}
'''
