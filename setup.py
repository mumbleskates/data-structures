# coding=utf-8
from setuptools import setup

setup(
    name="data-structures",
    description="Codefellows 401 data structures project",
    version=0.1,
    author="Kent Ross, Jeremy Edwards",
    author_email="",
    license="MIT",
    packages=["data_structures"],
    package_dir={"": "src"},
    install_requires=[
        'future==0.17.1',
    ],
    extras_require={
        'test': [
            'coverage==4.5.4',
            'mock==3.0.5',
            'pytest==5.2.1',
            'pytest-cov==2.8.1',
            'tox==3.14.0',
        ]
    },
)
