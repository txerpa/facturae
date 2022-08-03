# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

from facturae import __version__

with open("requirements/requirements.txt", "r") as f:
    INSTALL_REQUIRES = f.readlines()

with open("requirements/requirements-dev.txt", "r") as f:
    TESTS_REQUIRES = f.readlines()

setup(
    name="facturae",
    version=__version__,
    url="http://www.gisce.net",
    author="GISCE-TI, S.L.",
    author_email="devel@gisce.net",
    original_author="Electrica Sollerense, S.A.U.",
    original_author_email="informatica@el-gas.es",
    packages=find_packages(exclude=["tests*"]),
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRES,
    license="GPLv3",
    description="Facturae",
    long_description=open("README.md").read(),
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
)
