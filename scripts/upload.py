#!/usr/bin/python3

"""
this script uploads your module to pypi

It does the following:
- clean
- setup.py sdist
- twine upload
- clean again

This script could be done via setuptools using the following:
- python3 setup.py sdist upload -r pypi --identity="Mark Veltzer" --sign
but this has bad security implications as it sends user and password plain text.
This is the reason we use twine(1) to upload the package.
On ubuntu twine(1) is from the 'twine' official ubuntu package.

References:
- https://pypi.python.org/pypi/twine
- https://python-packaging-user-guide.readthedocs.org/en/latest/index.html
- http://peterdowns.com/posts/first-time-with-pypi.html
"""

import os
import os.path
import common

do_use_setup = True
do_use_twine = False
    

def upload_by_setup():
    common.check_call_no_output([
        'python',
        'setup.py',
        'sdist',
        'upload',
        '-r',
        'pypi',
    ])
    common.git_clean_full()


def upload_by_twine():
    common.check_call_no_output([
        'python3',
        'setup.py',
        'sdist',
    ])
    # at this point there should be only one file in the 'dist' folder
    file_list = list(os.listdir('dist'))
    assert len(file_list) == 1
    filename = file_list[0]
    full_filename = os.path.join('dist', filename)
    common.check_call_no_output([
        'twine',
        'upload',
        full_filename,
        # '--config-file',
        # common.config_file,
    ])

common.git_clean_full()
try:
    if do_use_setup:
        upload_by_setup()
    if do_use_twine:
        upload_by_twine()
finally:
    common.git_clean_full()
