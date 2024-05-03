import os
from setuptools import setup, find_packages

__version__ = '0.1.0'


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pyscan",
    version=__version__,
    author="Andrew M. Mounce, Michael P. Lilly, Jasmine J. Mah",
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
        # if ipykernel fails, force specific python version that will work rather than omitting ipykernel requirement.
        'ipykernel',
        'pytest',
    ],
    extras_require={'oceanoptics': ['seabreeze']},
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
)
