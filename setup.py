#!/usr/bin/env python

from setuptools import setup, find_packages


with open("README.rst") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="url-signer",
    version="0.0.4",
    description="The simplest way to sign the url",
    long_description=readme,
    author="Ilya Levin",
    author_email="ilya.levin@kaminario.com",
    url="https://github.com/Kaminario/signer",
    license=license,
    packages=find_packages(),
    install_requires=("python-baseconv>=1.2.0",),
    classifiers=[
        "Development Status :: 1 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
