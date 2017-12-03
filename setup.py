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
        'future==0.16.0',
    ],
    extras_require={
        'test': [
            'coverage==4.4.2',
            'mock==2.0.0',
            'pytest==3.3.0',
            'pytest-cov==2.5.1',
            'tox==2.9.1',
        ]
    },
)
