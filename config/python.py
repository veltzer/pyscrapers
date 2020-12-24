import config.project

package_name = config.project.project_name

console_scripts = [
    'pyscrapers=pyscrapers.main:main',
]

setup_requires = [
]

install_requires = [
    'lxml',
    'requests',
    # 'hyper',
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
    'pytest-cov',
    'pyflakes',
    'pyre-check',
    'flake8',
    'pymakehelper',
]


dev_requires = [
    'pyclassifiers',
    'pypitools',
    'pydmt',
    'Sphinx',
]

python_requires = ">=3.7"

extras_require = {
}

test_os = "[ubuntu-16.04, ubuntu-18.04, ubuntu-20.04]"
test_python = "[3.7, 3.8]"
test_container = "[ 'ubuntu:18.04', 'ubuntu:20.04' ]"
