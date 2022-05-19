<%!
    import pydmt.helpers.misc
    import pydmt.helpers.project
    import pydmt.helpers.python
    import pydmt.helpers.urls
    import config.python
    import user.personal
    import config.project
    import config.version
    import pydmt.helpers.python
%>import setuptools


def get_readme():
    with open('README.rst') as f:
        return f.read()


setuptools.setup(
    # the first three fields are a must according to the documentation
    name="${pydmt.helpers.project.get_name()}",
    version="${pydmt.helpers.misc.get_version_str()}",
    packages=${pydmt.helpers.python.array_indented(1, pydmt.helpers.python.find_packages(pydmt.helpers.python.get_package_name()))},
    # from here all is optional
    description="${config.project.description_short}",
    long_description=get_readme(),
    long_description_content_type="text/x-rst",
    author="${user.personal.fullname}",
    author_email="${user.personal.email}",
    maintainer="${user.personal.fullname}",
    maintainer_email="${user.personal.email}",
    keywords=${pydmt.helpers.python.array_indented(1, config.project.keywords)},
    url="${pydmt.helpers.urls.get_website()}",
    download_url="${pydmt.helpers.urls.get_website_source()}",
    license="${pydmt.helpers.python.get_license_type()}",
    platforms=${pydmt.helpers.python.array_indented(1, pydmt.helpers.python.get_platforms())},
% if hasattr(config.python, "install_requires"):
    install_requires=${pydmt.helpers.python.array_indented(1, config.python.install_requires)},
% endif
% if hasattr(config.python, "extras_requires"):
    extras_require=${pydmt.helpers.python.dict_indented(1, config.python.extras_require)},
% endif
    classifiers=${pydmt.helpers.python.array_indented(1, pydmt.helpers.python.get_classifiers())},
% if hasattr(config.python, "data_files"):
    data_files=${pydmt.helpers.python.array_indented(1, config.project.data_files)},
% endif
% if hasattr(config.python, "console_scripts"):
    entry_points={"console_scripts": ${pydmt.helpers.python.array_indented(1, config.python.console_scripts)}},
% endif
% if hasattr(config.python, "python_requires"):
    python_requires="${config.python.python_requires}",
% endif
)
