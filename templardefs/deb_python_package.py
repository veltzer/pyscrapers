"""
packaging definitions
"""


def populate(d):
    # deb section
    d.deb_package = True
    d.deb_section = 'python'
    d.deb_priority = 'optional'
    d.deb_architecture = 'all'
    d.deb_pkgname = 'pyscrapers'
    # to which series to publish the package?
    d.deb_series = [
        'artful',
        'zesty',
        'xenial',
        'trusty',
    ]
    d.deb_depends = '${misc:Depends}, ${python3:Depends}, python3-mako'
    d.deb_builddepends = 'python3, python3-setuptools, debhelper, dh-python'
    d.deb_standards_version = '3.9.8'
    d.deb_x_python_version = '>= 3.4'
    d.deb_x_python3_version = '>= 3.4'
    d.deb_urgency = 'low'
    d.entry_points = {
        'console_scripts': [
            'pyscrapers_photos=pyscrapers.scripts.photos:main',
        ],
    }


def get_deps():
    return [
        __file__,  # myself
    ]
