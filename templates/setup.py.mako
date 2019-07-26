<%!
    import config.python
    import user.personal
    import config.project
    import config.version
    import config.helpers
%>import setuptools

"""
The documentation can be found at:
http://setuptools.readthedocs.io/en/latest/setuptools.html
"""
setuptools.setup(
    # the first three fields are a must according to the documentation
    name='${config.project.project_name}',
    version='${config.version.version_str}',
    packages=${config.helpers.array_indented(1, config.helpers.find_packages(config.python.package_name))},
    # from here all is optional
    description='${config.project.project_description}',
    long_description='${config.project.project_long_description}',
    author='${user.personal.personal_fullname}',
    author_email='${user.personal.personal_email}',
    maintainer='${user.personal.personal_fullname}',
    maintainer_email='${user.personal.personal_email}',
    keywords=${config.helpers.array_indented(1, config.project.project_keywords)},
    url='${config.project.project_website}',
    download_url='${config.project.project_website_download_src}',
    license='${config.project.project_license}',
    platforms=${config.helpers.array_indented(1, config.project.project_platforms)},
    install_requires=${config.helpers.array_indented(1, config.python.install_requires)},
    classifiers=${config.helpers.array_indented(1, config.project.project_classifiers)},
    data_files=${config.helpers.array_indented(1, config.project.project_data_files)},
    entry_points={'console_scripts': ${config.helpers.array_indented(1, config.python.console_scripts)}},
    python_requires='${config.python.python_requires}',
)
