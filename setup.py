import sys
from setuptools import setup, find_packages
from pathlib import Path
import os


def get_requiremntss(file_path):
    """
    This function will return the list of requirements
    """
    with open(file_path) as requirement_file:

        requirements = requirement_file.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        if '-e .' in requirements:
            requirements.remove('-e .')
    return requirements
project_name = "mlproject"
setup(
    name=project_name,
    version="0.0.1",
    author="Ali Ahmad",
    author_email="aliahmaddawana@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    description="A machine learning project",
    install_requires=get_requiremntss('requirements.txt'),
)