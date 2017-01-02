#!/usr/bin/python3

import shutil
import subprocess
import os

dist_folder = 'dist'

if os.path.isdir(dist_folder):
    shutil.rmtree(dist_folder)
subprocess.check_call([
    'python3',
    'setup.py',
    '--quiet',
    'sdist',
])
files = list(os.listdir(dist_folder))
assert len(files) == 1
new_file = os.path.join(dist_folder, files[0])
subprocess.check_call([
    'sudo',
    '-H',
    'pip3',
    'install',
    '--quiet',
    '--upgrade',
    new_file,
])
