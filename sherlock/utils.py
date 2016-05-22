# utils

import os
import re
import string
import time
import subprocess
import shutil

#-------------#
# Other utils #
#-------------#

def get_selection():
    """ get clipboard content """
    cb = subprocess.Popen(["xclip", "-selection", "primary", "-o"], stdout=subprocess.PIPE).communicate()[0]

    return cb.decode('utf8').strip()


def run_cmd(cmd):
    if isinstance(cmd, str):
        cmd = cmd.split()

    return subprocess.call(cmd)


def get_cmd_output(cmd_list):
    try:
        output = subprocess.check_output(cmd_list, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return ''

    return output.decode('utf8').strip()


def is_running(name):
    processes = str(subprocess.check_output(('ps', '-u', os.environ['USER'], '-o', 'comm',
                                             '--no-headers')), encoding='utf8').rstrip('\n').split('\n')
    return (name in processes)


def copy_file(src, dest):
    try:
        shutil.copy(src, dest)
    except shutil.Error as e:
        print('Error: %s' % e)
    except IOError as e:
        print('Error: %s' % e.strerror)

# def xselSetClipboard(text):
#     p = Popen(['xsel', '-i'], stdin=PIPE)
#     try:
#         # works on Python 3 (bytes() requires an encoding)
#         p.communicate(input=bytes(text, 'utf-8'))
#     except TypeError:
#         # works on Python 2 (bytes() only takes one argument)
#         p.communicate(input=bytes(text))
