# -*- coding: utf-8 -*-
"""
    Flask-Waf
    ---------

    Adds server Waf support to your application.

    :copyright: (c) 2018 by Virink
    :license: BSD, see LICENSE for more details.
"""
from setuptools import setup


setup(
    name='Flask-Waf',
    version='1.0',
    url='https://github.com/virink/webwaf/flask',
    license='BSD',
    author='Virink',
    author_email='virink@outlook.com',
    description='Just a webwaf for log',
    long_description=__doc__,
    packages=['flask_waf'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.8'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
