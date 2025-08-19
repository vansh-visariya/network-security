from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """ this will return u list of requirements"""
    require = []
    try:
        with open('requirements.txt','r') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip() ## remove /n
                if requirement and requirement!="-e .":  ## remove -e .
                    require.append(requirement)
    except FileNotFoundError:
        print("requirements.txt not found")

    return require

setup(
    name = "NetworkSecurity",
    version = "0.1",
    author = "vansh visariya",
    packages = find_packages(),
    install_requires = get_requirements()
)