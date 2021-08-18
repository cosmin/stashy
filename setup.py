import os
from setuptools import setup

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fhandle:
        return fhandle.read()

def readlines(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fhandle:
        return fhandle.readlines()

setup(name='stashy',
      version="0.8",
      description='Python API client for the  Atlassian Bitbucket Server (formerly known as Stash) REST API',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      url='http://github.com/cosmin/stashy',
      download_url = 'https://github.com/cosmin/stashy',
      author='Cosmin Stejerean',
      author_email='cosmin@offbytwo.com',
      license='Apache License 2.0',
      packages=['stashy', 'stashy.admin'],
      test_suite = 'tests',
      #scripts=['bin/stash'],
      install_requires=readlines('requirements.txt'),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        ]
     )
