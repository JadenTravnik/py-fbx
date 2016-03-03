#!/usr/bin/env python

from distutils.core import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='pyfbx',
    version='0.1.0',
    description="A simple-to-use Python wrapper for FBX",
    long_description=long_description,
    author='Jo Chasinga',
    author_email='jo.chasinga@gmail.com',
    packages=['pyfbx'],
    include_package_data=True,
    install_requires=[
        'pytest',
    ],
    zip_safe=False,
    url='https://github.com/jochasinga/pyfbx',
    download_url = 'https://github.com/jochasinga/pyfbx/tarball/0.1.0',
    keywords = ['autodesk', 'fbx', 'maya', 'filmbox', '3d'],
    classifiers=[
        'Development Status :: Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers :: Digital Artists',
        'License :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Topic :: 3d digital media',
    ],
)

