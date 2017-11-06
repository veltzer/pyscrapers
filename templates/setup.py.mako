import setuptools

# noinspection PyPep8
setuptools.setup(
    name='${tdefs.project_name}',
    version='0.0.3',
    description='${tdefs.project_description}',
    long_description='${tdefs.project_long_description}',
    author='${tdefs.personal_fullname}',
    author_email='${tdefs.personal_email}',
    maintainer='${tdefs.personal_fullname}',
    maintainer_email='${tdefs.personal_email}',
    keywords=${tdefs.project_keywords},
    url='${tdefs.project_website}',
    download_url='${tdefs.project_website_download}',
    license='${tdefs.project_license}',
    platforms=${tdefs.project_platforms},
    packages=setuptools.find_packages(),
    # include_package_data=True,
    install_requires=${tdefs.requirements3},
    # noinspection PyBroadException,PyPep8
    classifiers=${tdefs.project_classifiers},
    data_files=${tdefs.project_data_files},
    entry_points=${tdefs.entry_points},
)
