import config.project

package_name = config.project.project_name

console_scripts = [
        'pyscrapers=pyscrapers.endpoints.main:main',
]

setup_requires = [
]

install_requires = [
    'lxml',
    'requests',
    'browser-cookie3',
    'pytconf',
    'pylogconf',
    'pornhub-api',
    'youtube-dl',
    'pyeventroute',
]

test_requires = [
    'pylint',
    'pytest',
    'pyflakes',
    'pyre-check',
    'flake8',
]


dev_requires = [
    'pyclassifiers',
    'pypitools',
    'pydmt',
    'Sphinx',
]

python_requires = ">=3.6"

extras_require = {
}

# deb section
deb_package = True
deb_section = 'python'
deb_priority = 'optional'
deb_architecture = 'all'
deb_package_name = 'pyscrapers'
# to which series to publish the package?
deb_series = [
    'artful',
    'zesty',
    'xenial',
    'trusty',
]
deb_depends = '${misc:Depends}, ${python3:Depends}, python3-mako'
deb_builddepends = 'python3, python3-setuptools, debhelper, dh-python'
deb_standards_version = '3.9.8'
deb_x_python_version = '>= 3.4'
deb_x_python3_version = '>= 3.4'
deb_urgency = 'low'
test_os = "[ubuntu-16.04, ubuntu-18.04, ubuntu-20.04]"
test_python = "[3.6, 3.7, 3.8]"
test_container = "[ 'ubuntu:18.04', 'ubuntu:20.04' ]"
