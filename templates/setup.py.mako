<%!
    import config.python
    import config.personal
    import config.project
    import config.version
    import config.helpers
%>import setuptools

setuptools.setup(
    name='${config.project.project_name}',
    version='${config.version.version_str}',
    description='${config.project.project_description}',
    long_description='${config.project.project_long_description}',
    author='${config.personal.personal_fullname}',
    author_email='${config.personal.personal_email}',
    maintainer='${config.personal.personal_fullname}',
    maintainer_email='${config.personal.personal_email}',
    keywords=${config.helpers.array_indented(1, config.project.project_keywords)},
    url='${config.project.project_website}',
    download_url='${config.project.project_website_download_src}',
    license='${config.project.project_license}',
    platforms=${config.helpers.array_indented(1, config.project.project_platforms)},
    packages=setuptools.find_packages(),
    install_requires=${config.helpers.array_indented(1, config.python.install_requires)},
    classifiers=${config.helpers.array_indented(1, config.project.project_classifiers)},
    data_files=${config.helpers.array_indented(1, config.project.project_data_files)},
    entry_points={'console_scripts': ${config.helpers.array_indented(1, config.python.console_scripts)}},
)
