# Pyscan

Python scientific measurement toolbox

## Intro

Pyscan is an instrument control and measurement tool box for scientific laboratory instruments.

It provides tools to create "experiments," in which you can interface with devices, define a measurement function with which to collect data from the devices, and run an experiment to "loop" over multiple variables or properties. The data can be plotted live so the experimenter can observe data collection during the experiment, and once complete, the data and metadata with all experimental parameters are automatically saved to a h5py file. Such files can be loaded and the data can be plotted again at a later time.

A selection of instrument drivers are included, but drivers from other libraries can also be used with pyscan.

## Contents

- [Pyscan](#pyscan)
  - [Intro](#intro)
  - [Contents](#contents)
  - [Getting Started](#getting-started)
    - [Requirements](#requirements)
    - [Install](#install)
    - [Usage](#usage)
  - [Contribute](#contribute)
  - [License](#license)
  - [Citing Pyscan](#citing-pyscan)

## Getting Started

Pyscan can be installed by downloading this repository and following the instructions below.

### Requirements

* Jupyter Lab (recommended interface to run experiments using pyscan), automatically installed through [Anaconda](https://www.anaconda.com)
* It is also recommended to install and use pyscan in a virtual environment
* conda or python must be accessable from the terminal or anaconda prompt

### Install

1. Use git to clone this repository into your computer.

2. Open a terminal or anaconda prompt window. Navigate to the pyscan folder, which contains the file "setup.py".

3. Install pyscan with

```
pip install -e .
```

### Usage

Sample Jupyter Notebooks running dummy experiments are located in the demo_notebooks folder.

For the full instructions on how to use pyscan library, [read the docs](https://pyscan.readthedocs.io/en/latest/)!

## Contribute

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

For questions please contact: Andy Mounce amounce@sandia.gov

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Citing Pyscan

If Pyscan contributes to a project that leads to publication, please acknowledge this using:

"Part of this work was enabled by the use of pyscan (github.com/sandialabs/pyscan), scientific measurement software made available by the Center for Integrated Nanotechnologies, an Office of Science User Facility operated for the U.S. Department of Energy."
