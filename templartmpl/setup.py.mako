"""
This is the installation tool. use minimal packages here.
don't use setuptools, don't use subprocess.
"""

import setuptools

import sys
if not sys.version_info[0] == 3:
    sys.exit("Sorry, only python version 3 is supported")

setuptools.setup(
    name='${tdefs.project_name}',
    version='${tdefs.git_lasttag}',
    description='${tdefs.project_description}',
    long_description='${tdefs.project_long_description}',
    author='${tdefs.personal_fullname}',
    author_email='${tdefs.personal_email}',
    maintainer='${tdefs.personal_fullname}',
    maintainer_email='${tdefs.personal_email}',
    keywords=${tdefs.project_keywords},
    url='${tdefs.project_website}',
    license='${tdefs.project_license}',
    platforms=${tdefs.project_platforms},
    packages=setuptools.find_packages(),
    #include_package_data=True,
    classifiers=${tdefs.project_classifiers},
    data_files=${tdefs.project_data_files},
    entry_points=${tdefs.entry_points},
)
