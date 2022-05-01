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

extras_require = {
}

python_requires = ">=3.9"
test_os = [ "ubuntu-20.04" ]
test_python = [ "3.9" ]
test_container = [ "ubuntu:20.04" ]
