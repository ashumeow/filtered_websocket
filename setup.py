import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "filtered_websocket",
    version = "0.0.0",
    author = "Morgan Reece Phillips",
    author_email = "winter2718@gmail.com",
    description = ("A simple framework for constructing websocket servers"
                                   "from filter chains."),
    license = "BSD",
    keywords = "websocket TwistedWebsocket",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=['filtered_websocket',],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
