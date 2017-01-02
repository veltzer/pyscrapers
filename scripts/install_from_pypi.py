#!/usr/bin/python3

import os
import subprocess
import common


# PIP="pip"
PIP = "pip3"
module = os.path.basename(os.getcwd())
common.check_call_no_output([
    "sudo",
    "-H",
    "{PIP}".format(**vars()),
    "install",
    "--quiet",
    "--upgrade",
    "{module}".format(**vars()),
])
output = subprocess.check_output([
    "{PIP}".format(**vars()),
    "show",
    "{module}".format(**vars()),
]).decode()
for line in output.split("\n"):
    if line.startswith("Version"):
        print(line)
