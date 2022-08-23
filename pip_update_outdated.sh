#!/bin/sh
pip list --outdated\
         --format=freeze \
         | grep -v '^\-e' \
         | cut -d = -f 1  \
         | xargs -n1 pip install -U

# workaround for python3.10 pipenv => else raises FileNotFound for 'python'
export SETUPTOOLS_USE_DISTUTILS=stdlib

# setup.py => top lvl is 'src' => 'vdcap=src.vcap.app:cli',