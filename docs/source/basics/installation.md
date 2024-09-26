# Installation

Pyscan can be installed by downloading this repository and following the instructions below.

## Requirements

* Jupyter Lab (recommended interface to run experiments using pyscan), automatically installed through [Anaconda](https://www.anaconda.com)
* It is also recommended to install and use pyscan in a virtual environment
* conda or python must be accessible from the terminal or anaconda prompt

## Install

1. Use git to clone this repository into your computer.
```
git clone https://github.com/sandialabs/pyscan
```

2. Open a terminal or anaconda prompt window. Navigate to the pyscan folder that you just downloaded, which contains the file `setup.py`.

3. Install pyscan with

```
pip install .
```

## Additional Requirements

Some instruments require extra installations in order to use them. For example, Ocean Optics (now known as Ocean Insight) spectrometers require the python package `seabreeze`.  Thorlabs drivers may also require the installation of proprietary .dll files available on their website by installing Thorlabs Kinesis.