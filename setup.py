#!/usr/bin/env python3
# -*- coding: 'utf-8' -*-

""" Collector of Polish data of COVID19 disease cases by the SARS-CoV-2. """
import os
import setuptools
from covid19pl.__version__ import __version__

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def current_dir():
    return os.path.dirname( os.path.abspath(__file__) )

config = {
    'author'            : 'oscarsierraproject.eu',
    'author_email'      : 'oscarsierraproject@protonmail.com',
    'maintainer'        : 'oscarsierraproject.eu',
    'maintainer_email'  : 'oscarsierraproject@protonmail.com',
    'contact'           : 'oscarsierraproject.eu',
    'contact_email'     : 'oscarsierraproject@protonmail.com',
    'classifiers'       : [
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: Polish',
        'Operating System :: POSIX :: Linux',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.7',
        # Indicate who your project is intended for
        'Topic :: Utilities',  
    ],
    'data_files'            : [
                                (":", [ "LICENSE", 
                                        "README.md", 
                                        "MANIFEST.in", 
                                        "requirements.txt"]
                                ),
                                ("data", ["covid19pl/data/*.json"] ),
                              ],
    'download_url'          : "https://github.com/oscarsierraproject/covid19pl",
    'description'           : "Collector of COVID19 disease cases in Poland.",
    'install_requires'      : [
                                "beautifulsoup4==4.8.2",
                                "bs4==0.0.1",
                                "matplotlib==3.2.1",
                                "python-dotenv==0.12.0",
                              ],
    'dependency_links'      : [],
    'keywords'              : 'disease, COVID19, SARS, SARS-CoV-2, Poland',
    'license'               : 'GNU General Public License 3.0',
    'name'                  : 'covid19pl',
    'packages'              : setuptools.find_packages(),
    'python_requires'       : ">3.7.3",
    'long_description'      : read('README.md'),
    'scripts'               : ['Makefile', './bin/*', './data/*'],
    'test_suite'            : "tests",
    'url'                   : 'https://github.com/oscarsierraproject/covid19pl',
    'version'               : __version__,
    
}

setuptools.setup(**config)
