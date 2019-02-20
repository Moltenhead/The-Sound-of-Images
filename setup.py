# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='soundofimages',
    version=1.0,
    packages=find_packages(),
    author="Charlie GARDAI / Moltenhead",
    author_email="ectopneo@gmail.com",
    description="Produce sounds, based on images",
    long_description=open('README.md').read(),
    install_requires=[
      'matplotlib>=1.4',
      'numpy>=1.16.1',
      'pyaudio>=0.2.11'
    ],
    url='https://github.com/Moltenhead/The-Sound-of-Images',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 2 - Expanding",
        "License :: GPL-3.0",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3+",
        "Topic :: Image perception and sound",
    ]
)
