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
    token_list = ['CI', 'TRAVIS', 'CONTINUOUS_INTEGRATION', 'USER']
    for token in token_list:
        print(os.getenv(token))
    ci_token = os.getenv('CI')
    if not ci_token:
        sigma = ApexSigma()
        sigma.run()
    else:
        exit(0)
