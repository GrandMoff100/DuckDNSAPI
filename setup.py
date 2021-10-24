from setuptools import setup
from duckdnsapi import (
    __name__,
    __description__,
    __author__,
    __author_email__,
    __version__,
)

setup(
    name=__name__,
    url="https://github.com/GrandMoff100/DuckDNSAPI",
    description=__description__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    long_description=open("README.rst", "r").read(),
    long_description_content_type="text/",
    packages=["duckdnsapi"],
    install_requires=["requests"]
)
