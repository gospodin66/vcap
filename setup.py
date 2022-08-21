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
        name="vcap",
        # Packages to include into the distribution
        packages=find_packages('src', include=['vcap*']), 
        package_dir={'vcap':'src/vcap'}, # the one line where all the magic happens
        # Start with a small number and increase it with every change you make
        # https://semver.org
        version=os.getenv('PACKAGE_VERSION', '0.0.1'),
        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
        # For example: MIT
        license='',
        # Short description of your library
        description='Tutorial package',
        # Long description of your library
        long_description = long_description,
        # Your name
        author='Cheki', 
        # Your email
        author_email='chekismail@fakeemail.com',     
        # Either the link to your github or to your website
        url='',
        # Link from which the project can be downloaded
        download_url='',
        # List of keyword arguments
        keywords=['vcap','videocap'],
        # List of packages to install with this one
        install_requires=[
            *read_pipenv_dependencies('Pipfile.lock')
        ],
        # https://pypi.org/classifiers/
        classifiers=[
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 2.7',
        ]  
    )

