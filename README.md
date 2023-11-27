# Pyscan

Python measurement toolbox

## Intro

Pyscan was developed to streamline the collection and live-assessment of data from laboratory instruments.

It provides tools to create "experiments," in which you can interface with devices, define a measurement function with which to collect data from the devices, and run an experiment to "loop" over multiple variables or properties. The data can be plotted live so the experimenter can observe data collection during the experiment, and once complete, the data and metadata with all experimental parameters are automatically saved to a h5py file. Such files can be loaded and the data can be plotted again at a later time.

A selection of instrument drivers are included, but drivers from other libraries can also be used with pyscan.

## Contents

- [Pyscan](#pyscan)
  - [Intro](#intro)
  - [Contents](#contents)
  - [Getting Started](#getting-started)
    - [Requirements](#requirements)
    - [Install](#install)
    - [Make your virtual environment accessible in Jupyter Lab](#make-your-virtual-environment-accessible-in-jupyter-lab)
    - [Usage](#usage)
  - [Contribute](#contribute)
  - [License](#license)
  - [Citing Pyscan](#citing-pyscan)

## Getting Started

Pyscan can be installed by downloading this repository and folloiwng the instructions below.

### Requirements

* Jupyter Lab (recommended interface to run experiments using pyscan), automatically installed through [Anaconda](https://www.anaconda.com)
* It is also recommended to install and use pyscan in a virtual environment
* conda or python must be accessable from the terminal or anaconda prompt

### Install

1. Use git to clone this repository into your computer.

```
https://gitlab-ex.sandia.gov/qsnmr/pyscan
```
2. Open a terminal or anaconda prompt window. Navigate to the pyscan folder, which contains the file "setup.py".

3. Recommended - Setup a new conda environment for pyscan and other data science tools:

```
conda create -n <environment-name>
```

Activate the virtual environment

```
conda activate <environment-name>
```
4. Ensure setuptools is installed and up to date

```
python -m pip install --upgrade setuptools
```

5. Install pyscan

```
pip install .
```

### Make your virtual environment accessible in Jupyter Lab

If you are using a conda virtual environment, run these steps to make your environment accessible as a kernel when you use Jupyter Lab (either activated from the Anaconda GUI or launched from the terminal in the conda base environment).

```
$ conda activate cenv          
(cenv)$ conda install ipykernel
(cenv)$ ipython kernel install --user --name=<any_name_for_kernel>
(cenv)$ conda deactivate
```

### Usage

Sample Jupyter Notebooks running dummy experiments are located in the demo_notebooks folder.

For the full instructions on how to use pyscan library, read the docs! (Coming Soon)

## Contribute

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Citing Pyscan

If Pyscan contributes to a project that leads to publication, please acknowledge this by citing Pyscan.