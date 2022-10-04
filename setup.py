# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

from facturae import __version__

setup(
    name="facturae",
    version=__version__,
    url="http://www.gisce.net",
    author="Electrica Sollerense, S.A.U.",
    author_email="informatica@el-gas.es",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "lxml>=4.9.0",
        "libComXML==3.1.0",
        "signxml==2.10.1",
        "xades==0.2.4",
        "crypto==1.4.1",
        "xmlsig==0.1.9"
    ],
    zip_safe=False,
    keywords=["facturae"],
    license="GPLv3",
    description="Facturae",
    long_description=open("README.md").read(),
    python_requires=">=3.8",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
)
