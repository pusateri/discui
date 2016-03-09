import os
import sys
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "hyp",
    version = "0.3",
    author = "Tom Pusateri",
    author_email = "pusateri@bangj.com",
    maintainer = "Tom Pusateri",
    maintainer_email = "pusateri@bangj.com",
    description = ("A RESTful cli command to interact with hypd"),
    entry_points=dict(console_scripts=['hyp=hyp:main',]),
    zip_safe=False,
    license = "MIT",
    keywords = "cli REST hypd",
    url = "http://dnshyp.com",
    packages=['hyp', 'hypd_completion'],
    long_description=read('../README'),
    install_requires = [
	'requests',
	'tabulate',
    ],
)
