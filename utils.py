# utils

import subprocess

def get_selection():
    """ get clipboard content """
    return subprocess.Popen(["xclip","-selection", "clipboard", "-o"], stdout=subprocess.PIPE).communicate()[0]

def check_output(cmd_list):
    try:
        output = subprocess.check_output(cmd_list)
    except subprocess.CalledProcessError:
        return ''

    return output.decode('utf8').strip()
