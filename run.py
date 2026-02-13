#!/usr/bin/env python

import errno
import os
import subprocess
import sys
import argparse

MIN_PY_VERSION = (3, 10)

try:
    from sigma.core.sigma import ApexSigma
except (ImportError, ModuleNotFoundError) as err:
    print(f"Missing module: {err}")

requirements_reinstalled = False

parser = argparse.ArgumentParser()
parser.add_argument('--count', type=int)
parser.add_argument('--group', type=str)
parser.add_argument('--restart', action='store_true')
args = parser.parse_args()

if not sys.version_info >= MIN_PY_VERSION:
    print('Fatal Error: Wrong Python Version! Sigma supports Python {}+!'.format('.'.join(map(str, MIN_PY_VERSION))))
    exit(errno.EINVAL)


def install_requirements():
    """
    Tries to install the pip requirements
    if startup fails due to a missing module.
    """
    global requirements_reinstalled
    pip_cmd = ['pip', 'install', '-Ur', 'requirements.txt']
    print('Missing required modules, attempting to install them...')
    try:
        subprocess.run(pip_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        requirements_reinstalled = True
    except (OSError, subprocess.SubprocessError):
        print('Requirement update failed!')
        exit(errno.EINVAL)


def import_framework():
    """
    Attempts to import the ApexSigma class.
    This is necessary after running `install_requirements`.
    :return:
    :rtype: ApexSigma
    """
    try:
        from sigma.core.sigma import ApexSigma
        return ApexSigma()
    except (ImportError, ModuleNotFoundError) as e:
        print('Installing missing requirements did not resolve the issue, please contact Sigma\'s developers.')
        print(repr(e))
        exit(errno.EINVAL)


def are_all_running(processes) -> bool:
    return all([process.is_alive() is None for process in processes])


def run():
    """
    The main run call.
    Runs the entire client core.
    """
    ci_token = os.getenv('CI')
    failures = 0
    if not ci_token:
        # noinspection PyBroadException
        try:
            # if `install_requirements` was run, reimport the framework.
            if requirements_reinstalled:
                sigma = import_framework()
            else:
                shard_count = args.count
                shard_group = args.group
                if shard_group and shard_count:
                    shard_group = [int(shard.strip()) for shard in shard_group.split(',') if shard.strip()]
                    sigma = ApexSigma(shard_count, shard_group)
                else:
                    sigma = ApexSigma()
            sigma.run()
        except (ImportError, ModuleNotFoundError, NameError):
            install_requirements()
            run()
        except KeyboardInterrupt:
            exit(1)
        except Exception:
            if args.restart:
                if failures < 5:
                    failures += 1
                    run()
    else:
        exit(0)


if __name__ == '__main__':
    restartable = args.restart
    if not restartable:
        run()
    else:
        # noinspection PyBroadException
        try:
            run()
        except Exception:
            pass
