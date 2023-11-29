import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pyscan",
    version="0.0.1",
    author="Andrew M. Mounce, Michael P. Lilly, Jasmine J. Mah",
    author_email="amounce@sandia.gov",
    description=(
        """
        Python measurement toolbox to interface with scientific
         instruments and run experements"""
        ),
    license="MIT",
    keywords="scientific instrument drivers measurement tools",
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
    ],
    extras_require={'oceanoptics': ['seabreeze']},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: MIT",
    ],
    python_requires='>=3.6',
)
