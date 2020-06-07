<%!
    import config.python
    import user.personal
    import config.project
    import config.version
    import pydmt.helpers.python
    import os
%>import setuptools


def get_readme():
    with open('README.rst') as f:
        return f.read()


setuptools.setup(
    # the first three fields are a must according to the documentation
    name="${config.project.project_name}",
    version="${config.version.version_str}",
% if os.path.isdir(config.python.package_name):
    packages=${pydmt.helpers.python.array_indented(1, pydmt.helpers.python.find_packages(config.python.package_name))},
% endif
% if os.path.isfile(config.python.package_name+".py"):
    py_modules=["${config.python.package_name}"],
% endif
    # from here all is optional
    description="${config.project.project_description}",
    long_description=get_readme(),
    long_description_content_type="text/x-rst",
    author="${user.personal.personal_fullname}",
    author_email="${user.personal.personal_email}",
    maintainer="${user.personal.personal_fullname}",
    maintainer_email="${user.personal.personal_email}",
    keywords=${pydmt.helpers.python.array_indented(1, config.project.project_keywords)},
    url="${config.project.project_website}",
    download_url="${config.project.project_website_download_src}",
    license="${config.project.project_license}",
    platforms=${pydmt.helpers.python.array_indented(1, config.project.project_platforms)},
    install_requires=${pydmt.helpers.python.array_indented(1, config.python.install_requires)},
    extras_require=${pydmt.helpers.python.dict_indented(1, config.python.extras_require)},
    classifiers=${pydmt.helpers.python.array_indented(1, config.project.project_classifiers)},
    data_files=${pydmt.helpers.python.array_indented(1, config.project.project_data_files)},
    entry_points={"console_scripts": ${pydmt.helpers.python.array_indented(1, config.python.console_scripts)}},
    python_requires="${config.python.python_requires}",
)
