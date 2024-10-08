import os
from setuptools import setup, find_packages
import json


def get_version():
    runinfo_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(runinfo_dir, "pyscan/VERSION.json")
    with open(path) as version_file:
        version = json.load(version_file)['version']
        if type(version) is str:
            return 'v' + version
        else:
            assert False, "no valid version found"


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pyscan",
    version=get_version(),
    author="Andrew M. Mounce, Michael P. Lilly, Jasmine J. Mah, Ryan S. Brost",
    author_email="amounce@sandia.gov",
    description=(
        """
        Python measurement toolbox to interface with scientific
        instruments and run experements"""
    ),
    license="MIT",
    keywords=[
        "scientific",
        "instrument",
        "drivers",
        "measurement",
        "experiment",
    ],
    url="",
    packages=find_packages(exclude=['docs']),
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    install_requires=[
        'pyvisa',
        'numpy >=1.21',
        'pandas',
        'pyserial',
        'ipywidgets',
        'h5py',
        'matplotlib',
        'jupyter',
        'pytest',
        'nbmake',
        'seabreeze',
        'pylablib',
        'pyscan-tlk'
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: MIT",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Physics",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix"
    ],
    python_requires='>=3.6',
    include_package_data=True,  # Ensure package data is included
    package_data={
        'pyscan': ['VERSION.json'],  # Specify the package data to include
    },
)
