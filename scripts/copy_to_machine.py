#!/usr/bin/python3

"""
This script copies important files to a machine

something like:
copy ~/.aws ~/.ssh ~/.s3cfg ~/.gitconfig ~/.passwd-s3fs to it
"""


import subprocess
import sys
import os.path

folders_to_copy = [
    "~/.aws",
    "~/.ssh",
    "~/.s3cfg",
    "~/.gitconfig",
    "~/.passwd-s3fs",
]

assert len(sys.argv) == 2
machine_name = sys.argv[1]
args = [
    "scp",
    "-r",
]
args.extend(map(os.path.expanduser, folders_to_copy))
args.append("ubuntu@{}:~".format(machine_name))
# subprocess.check_call(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.check_call(args)
