#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup
import digit

setup(name=digit.__name__,
      version=digit.__version__,
      author='Pongsakorn Sommalai',
      author_email='bongtrop@gmail.com',
      license='MIT',

      url='https://github.com/bongtrop/digit',
      description='Dig git information from .git',
      long_description=digit.__doc__,
      scripts=['digit.py'],
      py_modules=['digit'],
      install_requires=[
       'requests'
      ],
      entry_points="""
        [console_scripts]
        digit=digit:main
      """,
      keywords=''
     )
