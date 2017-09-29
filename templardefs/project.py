"""
project definitions
"""

# noinspection PyUnresolvedReferences,PyPackageRequirements
import templar.utils


def populate(d):
    d.project_github_username = 'veltzer'
    d.project_name = 'pyscrapers'
    d.project_website = 'https://{project_github_username}.github.io/{project_name}'.format(**d)
    d.project_website_source = 'https://github.com/{project_github_username}/{project_name}'.format(**d)
    d.project_website_git = 'git://github.com/{project_github_username}/{project_name}.git'.format(**d)
    d.project_website_download = 'https://launchpad.net/~mark-veltzer/+archive/ubuntu/ppa'
    # d.project_paypal_donate_button_id='ASPRXR59H2NTQ'
    # d.project_google_analytics_tracking_id='UA-56436979-1'
    d.project_long_description = 'project to produce various useful scrapers'
    d.project_short_description = 'project to produce various useful scrapers'
    # keywords to put on html pages or for search, dont put the name of the project or my details
    # as they will be added automatically...
    d.project_keywords = [
        'scape',
        'images',
        'social',
    ]
    d.project_license = 'MIT'
    d.project_year_started = '2016'
    d.project_description = '''What is Scrapers? Look in the "doc" subfolder of the source code...'''.format(**d)
    d.project_platforms = [
        'ALL',
    ]
    d.project_classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ]
    d.project_data_files = []
    d.project_data_files.append(templar.utils.hlp_files_under('/usr/bin', 'src/*'))


def get_deps():
    return [
        __file__,  # myself
    ]
