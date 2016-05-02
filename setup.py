#!/usr/bin/env python
from setuptools import setup

with open('requirements.txt') as reqs:
    requirements = filter(lambda s: s!='',
                          map(lambda s: s.strip(), reqs))

setup(name='SerpentTests',
      version='1.0',
      description='Serpent Contract Testing Class',
      author='ChrisCalderon',
      author_email='calderon.christian760@gmail.com',
      packages=['serpent_tests'],
      install_requires=requirements)
