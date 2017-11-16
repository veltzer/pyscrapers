"""
Attributes for this project
"""

import datetime
import subprocess
import os.path
import os
import glob
import socket
import pprint
import pyscrapers.core.config

'''
this function finds all the python packages under a folder and
write the 'packages' and 'package_dir' entries for a python setup.py
script
'''


def hlp_source_under(folder):
    # walk the folder and find the __init__.py entries for packages.
    packages = []
    package_dir = dict()
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file != '__init__.py':
                continue
            full = os.path.dirname(os.path.join(root, file))
            relative = os.path.relpath(full, folder)
            packages.append(relative)
            package_dir[relative] = full
    # we use pprint because we want the order to always remain the same
    return 'packages={0},\npackage_dir={1}'.format(sorted(packages), pprint.pformat(package_dir))


def hlp_files_under(destination_folder, pat):
    return '(\'{0}\', {1})'.format(destination_folder, [x for x in glob.glob(pat) if os.path.isfile(x)])


def make_hlp_project_keywords(d):
    def hlp_project_keywords():
        return '{0}'.format(d.project_keywords.split())

    return hlp_project_keywords


def make_hlp_project_platforms(d):
    def hlp_project_platforms():
        return '{0}'.format(d.project_platforms.split())

    return hlp_project_platforms


def make_hlp_project_classifiers(d):
    def hlp_project_classifiers():
        classifiers = d.project_classifiers.split('\n')
        classifiers = [x.strip()[1:-1] for x in classifiers]
        return '{0}'.format(classifiers)

    return hlp_project_classifiers


def make_hlp_wrap(level):
    def hlp_wrap(t):
        return t.replace('\n', '\n' + '\t' * level)

    return hlp_wrap


def populate(d):
    # general
    d.general_current_year = datetime.datetime.now().year
    d.general_homedir = os.path.expanduser('~')
    # d.general_hostname=subprocess.check_output(['hostname']).decode().rstrip()
    d.general_hostname = socket.gethostname()
    d.general_domain_name = subprocess.check_output(['hostname', '--domain']).decode().rstrip()

    # messages
    d.messages_dne = 'THIS FILE IS AUTO GENERATED. DO NOT EDIT!!!'

    # project
    if 'project_year_started' in d:
        d.project_copyright_years = ', '.join(
            map(str, range(int(d.project_year_started), datetime.datetime.now().year + 1)))
        if str(d.general_current_year) == d.project_year_started:
            d.project_copyright_years = d.general_current_year
        else:
            d.project_copyright_years = '{0}-{1}'.format(d.project_year_started, d.general_current_year)
    d.current_folder = os.path.basename(os.getcwd())

    if 'project_google_analytics_tracking_id' in d:
        d.project_google_analytics_snipplet = '''<script type="text/javascript">
(function(i,s,o,g,r,a,m){{i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){{
(i[r].q=i[r].q||[]).push(arguments)}},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
}})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

ga('create', '{0}', 'auto');
ga('send', 'pageview');

</script>'''.format(d.project_google_analytics_tracking_id)

    if 'project_paypal_donate_button_id' in d:
        d.project_paypal_donate_button_snipplet = '''<form action="https://www.paypal.com/cgi-bin/webscr"
        method="post" target="_top">
<input type="hidden" name="cmd" value="_s-xclick">
<input type="hidden" name="hosted_button_id" value="{0}">
<input type="image" src="https://www.paypalobjects.com/en_US/IL/i/btn/btn_donateCC_LG.gif" name="submit"
alt="PayPal - The safer, easier way to pay online!">
<img alt="" border="0" src="https://www.paypalobjects.com/en_US/i/scr/pixel.gif" width="1" height="1">
</form>'''.format(d.project_paypal_donate_button_id)

    # git
    # noinspection PyBroadException,PyPep8
    try:
        d.git_describe = subprocess.check_output(['git', 'describe'], stderr=subprocess.DEVNULL).decode().rstrip()
    except:
        d.git_describe = 'no git repository'

    # this is wrong for the tag since they may not be alphabetically ordered...
    # tag=subprocess.check_output(['git', 'tag']).decode().rstrip()
    # if tag!='':
    #    d.git_last_tag=tag.split()[-1].rstrip()
    # else:
    #    d.git_last_tag='no git tag yet'

    # this is right
    # noinspection PyBroadException,PyPep8
    try:
        d.git_last_tag = subprocess.check_output(['git', 'describe', '--abbrev=0', '--tags'],
                                                 stderr=subprocess.DEVNULL).decode().rstrip()
        d.git_describe = subprocess.check_output(['git', 'describe'], stderr=subprocess.DEVNULL).decode().rstrip()
        d.git_version = '.'.join(d.git_describe.split('-'))
    except:
        d.git_last_tag = '0'
        d.git_describe = '0'
        d.git_version = '0'

    # deb
    d.deb_package_name = os.path.basename(os.getcwd())
    # create this with 'date -R'
    # TODO: this should be created automatically here in python
    d.deb_date = 'Mon, 17 Oct 2016 09:44:00 +0300'

    # apt
    d.apt_protocol = 'https'
    d.apt_codename = subprocess.check_output(['lsb_release', '--codename', '--short']).decode().rstrip()
    d.apt_arch = subprocess.check_output('dpkg-architecture | grep -e ^DEB_BUILD_ARCH= | cut -d = -f 2',
                                         shell=True).decode().rstrip()
    d.apt_architectures = '{0} source'.format(d.apt_arch)
    d.apt_component = 'main'
    d.apt_folder = 'apt'
    d.apt_service_dir = os.path.join(d.general_homedir, 'public_html/public', d.apt_folder)
    d.apt_except = '50{0}'.format(d.personal_slug)
    d.apt_pack_list = glob.glob(os.path.join(d.general_homedir, 'packages', '*.deb'))
    d.apt_pack_str = ' '.join(d.apt_pack_list)
    d.apt_id = subprocess.check_output(['lsb_release', '--id', '--short']).decode().rstrip()
    d.apt_key_file = 'public_key.gpg'
    d.apt_apache_site_file = '{0}.apt'.format(d.personal_slug)

    # helper functions
    d.hlp_source_under = hlp_source_under
    d.hlp_files_under = hlp_files_under
    d.hlp_project_keywords = make_hlp_project_keywords(d)
    d.hlp_project_platforms = make_hlp_project_platforms(d)
    d.hlp_project_classifiers = make_hlp_project_classifiers(d)
    d.make_hlp_wrap = make_hlp_wrap

    # composites
    d.deb_version = '{0}~{1}'.format(d.git_version, d.apt_codename)

    d.types = pyscrapers.core.config.types

