'''
project definitions for templar
'''

def populate(d):
    d.project_github_username='veltzer'
    d.project_name='scrapers'
    d.project_website='https://{project_github_username}.github.io/{project_name}'.format(**d)
    d.project_website_source='https://github.com/{project_github_username}/{project_name}'.format(**d)
    d.project_website_git='git://github.com/{project_github_username}/{project_name}.git'.format(**d)
    #d.project_paypal_donate_button_id='ASPRXR59H2NTQ'
    #d.project_google_analytics_tracking_id='UA-56436979-1'
    d.project_long_description='Scrapers is a project to produce various useful scrapers'
    # keywords to put on html pages or for search, dont put the name of the project or my details
    # as they will be added automatically...
    d.project_keywords=[
            'scape',
            'images',
            'social',
    ]
    d.project_license='GPLV3'
    d.project_year_started='2016'
    d.project_description='''What is Scrapers?
Look in the "doc" subfolder of the source code...'''.format(**d)

    # deb
    d.deb_package=True

def getdeps():
    return [
        __file__, # myself
    ]
