#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='mosmetro',
      version='1.0',

      author='Dmitry Karikh',
      author_email='the.dr.hax@gmail.com',
      license='GNU GPLv3',
      url='https://github.com/mosmetro-android/mosmetro-python',

      install_requires=['requests', 'furl', 'user_agent', 'beautifulsoup4'],

      packages=find_packages(),
      include_package_data=True,

      entry_points='''
        [console_scripts]
        mosmetro=mosmetro.__main__:main
      ''',
     )
