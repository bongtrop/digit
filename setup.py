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
      download_url='https://github.com/bongtrop/digit/archive/v1.1.0.tar.gz',
      description='Dig git information from .git',
      long_description=open("README.md").read(),
      scripts=['digit/digit.py'],
      py_modules=['digit.digit'],
      install_requires=[
       'requests'
      ],
      entry_points="""
        [console_scripts]
        digit=digit:main
      """,
      keywords=['git', 'tool', 'hack'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Other Audience',
          'License :: OSI Approved :: MIT License',
          'Topic :: Utilities',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7']
     )
