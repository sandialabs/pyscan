Welcome to pyscan's documentation!
==================================

## Intro

**Pyscan** is a toolbox for controlling and collecting measurements from scientific laboratory instruments.

It provides tools to create "experiments," in which you can interface with devices, collect data from the devices using custom functions, and run the experiment to "loop" over multiple variables or properties. The data can be plotted live so the experimenter can observe data collection during the experiment, and once complete, the data and metadata with all experimental parameters are automatically saved to a h5py file. Such files can be loaded and the data can be plotted again at a later time.

A selection of instrument drivers are included, but drivers from other libraries can also be used with pyscan.

```{toctree}
:maxdepth: 1

the_basics
```

```{toctree}
:maxdepth: 1

advanced_usage
```

```{toctree}
:maxdepth: 2

api_index
```

# Indices and tables

```{eval-rst}
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

