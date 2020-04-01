#!/usr/bin/env python

__author__ = 'Xyene'
from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as fh:
    long_description = fh.read()

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'sphere2cube', 'version.py')) as version:
    exec (version.read())

setup(name='sphere2cube',
      version=__version__,
      description='Utility to map an equirectangular (cylindrical projection; skysphere) map into 6 cube (cubemap; skybox) faces',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Tudor Brindus',
      author_email='me@tbrindus.ca',
      url='http://github.com/Xyene/sphere2cube',
      packages=find_packages(),
      package_data={
          "sphere2cube": ["*.blend"],
      },
      entry_points={
          'console_scripts': ['sphere2cube=sphere2cube.sphere2cube:main'],
      },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Artistic Software'
      ],
)
