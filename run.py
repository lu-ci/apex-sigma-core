#!/usr/bin/env python3.6
import errno
import os
import sys

from sigma.core.sigma import ApexSigma

try:
    assert sys.version_info >= (3, 6)
except AssertionError:
    print('Fatal Error: Wrong Python Version! Sigma supports Python 3.6+!')
    exit(errno.EINVAL)

if __name__ == '__main__':
    sigma = ApexSigma()
    ci_token = os.getenv('CI_TOKEN')
    if ci_token:
        exit(0)
    else:
        sigma.run()
