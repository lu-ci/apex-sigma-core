#!/usr/bin/env python

import errno
import os
import subprocess
import sys
from multiprocessing import Process, Queue

try:
    from sigma.core.sigma import ApexSigma

    modules_missing = False
except (ImportError, ModuleNotFoundError):
    modules_missing = True

modules_installed = False

if not sys.version_info >= (3, 6):
    print('Fatal Error: Wrong Python Version! Sigma supports Python 3.6+!')
    exit(errno.EINVAL)


def install_requirements():
    """
    Tries to install the pip requirements
    if startup fails due to a missing module.
    :return:
    """
    global modules_installed
    if not modules_installed:
        pip_cmd = ['pip', 'install', '-Ur', 'requirements.txt']
        print('Missing required modules, trying to install them...')
        try:
            subprocess.run(pip_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            modules_installed = True
        except (OSError, subprocess.SubprocessError):
            print('Requirement update failed!')
            exit(errno.EINVAL)
    else:
        print('Trying to install missing requirements did not work, please contact Sigma\'s developers.')
        exit(errno.EINVAL)


def run(shard_id=None):
    """
    The main run call.
    Runs the entire client core.
    :return:
    """
    global modules_missing
    ci_token = os.getenv('CI')
    if not ci_token:
        try:
            try:
                shard_count = int(os.environ['SIGMA_SHARD_COUNT'])
            except (KeyError, ValueError):
                shard_count = None
            sigma = ApexSigma(shard_count)
            sigma.run(shard_id)
        except (ImportError, ModuleNotFoundError, NameError):
            modules_missing = True
            install_requirements()
            run()
    else:
        exit(0)


if __name__ == '__main__':
    try:
        shards = int(os.environ['SIGMA_SHARD_COUNT'])
    except (KeyError, ValueError):
        shards = None
    if shards:
        for shard in list(range(0, shards)):
            p = Process(target=run, args=(shard,))
            p.start()
    else:
        run()
