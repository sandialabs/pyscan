Welcome to pyscan's documentation!
==================================

# Pyscan

Python scientific measurement toolbox

## Intro

Pyscan is an instrument control and measurement tool box for scientific laboratory instruments.

It provides tools to create "experiments," in which you can interface with devices, define a measurement function with which to collect data from the devices, and run an experiment to "loop" over multiple variables or properties. The data can be plotted live so the experimenter can observe data collection during the experiment, and once complete, the data and metadata with all experimental parameters are automatically saved to a h5py file. Such files can be loaded and the data can be plotted again at a later time.

A selection of instrument drivers are included, but drivers from other libraries can also be used with pyscan.

```{toctree}
:maxdepth: 1

the_basics
```

```{toctree}
:maxdepth: 2

api_index
```
.. toctree::


# Indices and tables

```{eval-rst}
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

