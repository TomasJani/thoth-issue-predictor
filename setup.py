"""Setup for project."""
import os

from setuptools import setup


def get_install_requires():
    """Get requirements for adviser module."""
    with open("requirements.txt", "r") as requirements_file:
        res = requirements_file.readlines()
        return [req.split(" ", maxsplit=1)[0] for req in res if req]


def read(fname):
    """Read."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="thoth-issue-predicator",
    version="0.0.1",
    description="A useful module",
    author="Tomas Janicek",
    author_email="tomasjanicek221@gmail.com",
    packages=["thoth_issue_predictor"],
    install_requires=get_install_requires(),
    long_description=read("README.md"),
)
