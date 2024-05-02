Welcome to pyscan's documentation!
==================================

## Intro

**Pyscan** is a toolbox for controlling and collecting measurements from scientific laboratory instruments.

It provides tools to create "experiments," in which you can interface with devices, collect data from the devices using custom functions, and run the experiment to "loop" over multiple variables or properties. The data can be plotted live so the experimenter can observe data collection during the experiment, and once complete, the data and metadata with all experimental parameters are automatically saved to a h5py file. Such files can be loaded and the data can be plotted again at a later time.

A selection of instrument drivers are included, but drivers from other libraries can also be used with pyscan.

Get started and [install pyscan](./basics/installation)!

## Usage

Sample Jupyter Notebooks running dummy experiments are located in the [demo_notebooks](./basics/notebooks) folder.

For the full instructions on how to use pyscan library, read the docs!

```{toctree}
:maxdepth: 2

the_basics
```

```{toctree}
:maxdepth: 2

advanced_usage
```

```{toctree}
:maxdepth: 2

api_index
```

## Contribute

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

**Current development team:**
- Andy Mounce amounce@sandia.gov
- Jasmine Mah jjmah@sandia.gov
- Ryan Brost rsbrost@sandia.gov

**Past contributors:**
A special thanks to all pyscan contributors: [Pyscan Contributors](https://github.com/sandialabs/pyscan/wiki/Pyscan-wall-of-fame#past-and-current-contributors)

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Citing Pyscan

If Pyscan contributes to a project that leads to publication, please acknowledge this using:

"Part of this work was enabled by the use of pyscan (github.com/sandialabs/pyscan), scientific measurement software made available by the Center for Integrated Nanotechnologies, an Office of Science User Facility operated for the U.S. Department of Energy."

# Indices and tables

```{eval-rst}
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

