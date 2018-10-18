#!/usr/bin/env python3.6
import errno
import os
import sys

from sigma.core.sigma import ApexSigma

if not sys.version_info >= (3, 6):
    print('Fatal Error: Wrong Python Version! Spookgma supports Python 3.6+!')
    exit(errno.EINVAL)

if __name__ == '__main__':
    ci_token = os.getenv('CI')
    if not ci_token:
        sigma = ApexSigma()
        sigma.run()
    else:
        exit(0)
