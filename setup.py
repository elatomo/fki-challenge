# -*- coding: utf-8 -*-

from os import path
from setuptools import setup, find_packages

exec(open('fki_challenge/version.py').read())

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    readme = f.read()

setup(
    name='fki-challenge',
    version=__version__,
    description='fredknows.it coding challenge.',
    long_description=readme,
    author='José Fernández Ramos',
    author_email='el.atomo@gmail.com',
    url='https://github.com/elatomo/fki-challenge',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=[
        'Flask-RESTful==0.3.5',
        'Flask-Script==2.0.5',
        'peewee==2.8.0'
    ],
    test_suite='tests',
    tests_require=['coverage'],
    license='BSD',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Private :: Do Not Upload',
        'Programming Language :: Python :: 3'
    ]
)
