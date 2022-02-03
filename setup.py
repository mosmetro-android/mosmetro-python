#!/usr/bin/env python

from setuptools import setup, find_packages


with open('README.md', 'r') as fi:
    long_description = fi.read()


setup(
    name='mosmetro',
    version='0.1.1',

    author='Dmitry Karikh',
    author_email='the.dr.hax@gmail.com',

    description='Скрипт для автоматической авторизации в сетях московского (и не только) общественного транспорта',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mosmetro-android/mosmetro-python',
    license='GNU GPLv3',

    install_requires=[
        'requests',
        'furl',
        'user_agent',
        'beautifulsoup4'
    ],

    packages=find_packages(),
    include_package_data=True,

    entry_points='''
        [console_scripts]
        mosmetro=mosmetro.__main__:main
    ''',

    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Internet',
        'Topic :: Utilities'
    ]
)
