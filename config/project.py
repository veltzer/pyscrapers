"""
project definitions
"""

import pyclassifiers.values

project_github_username = 'veltzer'
project_name = 'pyscrapers'
github_repo_name = project_name
project_website = 'https://{project_github_username}.github.io/{project_name}'.format(**locals())
project_website_source = 'https://github.com/{project_github_username}/{project_name}'.format(**locals())
project_website_git = 'git://github.com/{project_github_username}/{project_name}.git'.format(**locals())
project_website_download_ppa = 'https://launchpanet/~mark-veltzer/+archive/ubuntu/ppa'
project_website_download_src = project_website_source
# project_paypal_donate_button_id='ASPRXR59H2NTQ'
# project_google_analytics_tracking_id='UA-56436979-1'
project_long_description = 'project to produce various useful scrapers'
project_short_description = 'project to produce various useful scrapers'
# keywords to put on html pages or for search, dont put the name of the project or my details
# as they will be added automatically...
project_keywords = [
    'scrape',
    'images',
    'social',
    'facebook',
    'instagram',
    'vk.com',
    'download',
    'pics',
]
project_license = 'MIT'
project_year_started = '2016'
project_description = 'A collection of scrapers for the web'
project_platforms = [
    'python3',
]
project_classifiers = [
    pyclassifiers.values.DevelopmentStatus__4_Beta,
    pyclassifiers.values.Environment__Console,
    pyclassifiers.values.OperatingSystem__OSIndependent,
    pyclassifiers.values.ProgrammingLanguage__Python,
    pyclassifiers.values.ProgrammingLanguage__Python__3,
    pyclassifiers.values.ProgrammingLanguage__Python__3__Only,
    pyclassifiers.values.Topic__Utilities,
    pyclassifiers.values.License__OSIApproved__MITLicense,
]
project_data_files = []
# project_data_files.append(templar.utils.hlp_files_under('/usr/bin', 'src/*'))
