from distutils.core import setup
from setuptools import find_packages

import os
import json

# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

def read_pipenv_dependencies(fname):
    """Get default dependencies from Pipfile.lock."""
    filepath = os.path.join(os.path.dirname(__file__), fname)
    with open(filepath) as lockfile:
        lockjson = json.load(lockfile)
        return [dependency for dependency in lockjson.get('default')]


if __name__ == '__main__':
    setup(
        # Name of the package
        name="vdcap",
        package_dir={'vcap':'src/vcap'}, # the one line where all the magic happens
        packages=find_packages('src', include=['*cap']), 
        version=os.getenv('PACKAGE_VERSION', '0.0.1'),
        description='Tutorial package',
        long_description = long_description,
        author='Cheki', 
        author_email='chekismail@fakeemail.com',     
        keywords=['vcap','videocap','vdcap'],
        install_requires=[
            *read_pipenv_dependencies('Pipfile.lock')
        ],
        entry_points={
            'console_scripts': [
                'vdcap=src.vcap.app:cli',
            ],
        },
        classifiers=[
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 2.7',
        ]  
    )

