import subprocess
import os.path

config_file = os.path.expanduser('~/.pypirc')


def check_call_no_output(args):
    p = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    (res_stdout, res_stderr) = p.communicate()
    if p.returncode:
        res_stdout = res_stdout.decode()
        res_stderr = res_stderr.decode()
        print(res_stdout, end='')
        print(res_stderr, end='')
        raise ValueError(p.returncode)


def git_clean_full():
    check_call_no_output([
        'git',
        'clean',
        '-qffxd',
    ])
