# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '1.0a1'
description = 'A carousel tile for collective.cover based on the Cycle2 slideshow plugin for jQuery.'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='covertile.cycle2',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='plone tile cycle2 slideshow carousel',
    author='Simples Consultoria',
    author_email='produts@simplesconsultoria.com.br',
    url='https://github.com/collective/covertile.cycle2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['covertile'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'collective.js.cycle2',
        'collective.cover',
        'Products.CMFPlone >=4.3',
        'Products.GenericSetup',
        'setuptools',
        'zope.i18nmessageid',
        'zope.interface',
    ],
    extras_require={
        'test': [
            'plone.app.robotframework',
            'plone.app.testing [robot] >=4.2.2',
            'plone.browserlayer',
            'plone.testing',
            'robotsuite',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
