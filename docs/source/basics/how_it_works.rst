How it works
============

Pyscan is organized around the concept of **experiments**. You can set up an experiment with pyscan, then run it. 
Watch the data being collected live using built-in plotting functions. Your data will be automatically 
saved and you can load and plot the data again afterwards.

.. image:: /_static/Pyscan_overview_C1_diagram.png
  :width: 600
  :alt: Pyscan Overview

What does an Experiment do?
---------------------------

An :class:`.Experiment` will:

* Interface with devices
* Collect data from devices using a custom function
* "Loop" over mutliple variables or properties (e.g. x, y, or z axes of a stage), collecting data at each point
* Allow you to live-plot the data as it is being collected
* Automatically save the data and experimental metadata to an h5py file

How to set up an Experiment
---------------------------

There are two required parameters to set up an experiment:

* Devices
* Runinfo

**Devices** is an :class:`.ItemAttribute` instance which contains an instance of a driver class 
for each instrument you would like to control or to read data from.

**Runinfo** is a :class:`.RunInfo` instance which contains instructions for how the experiment should run.

.. note::
    The :class:`.ItemAttribute` class is a core building block of pyscan. It is essentially a class that 
    contains dictionary methods, so you can call ``ItemAttribute.keys()`` or ``ItemAttribute.items()`` 
    just like you can with a dictionary. However, you can also still use dot notation since it is actually
    a class, e.g. ``ItemAttribute.myattribute = 3`` and ``ItemAttribute["myattribute"] == 3``.

.. image:: /_static/Runinfo_Devices_and_Experiment.png
  :width: 600
  :alt: Runinfo Devices and Experiment

Devices
-------

Search for your instrument from the instrument classes listed in :doc:`/api/drivers`. You must create an
instance of your desired driver class, such as :class:`.Stanford830` and set that as an attribute of devices:

.. code-block:: python

    devices = ps.ItemAttribute()
    devices.sr830 = ps.Stanford830()


The main style of driver uses the ``pyvisa`` python library to connect and communicate with instruments.
Any instrument which has a GPIB, RS-232 Serial, USB or Ethernet connection and supports SCPI commands
can usually be interfaced with pyvisa.

Certain instruments provide .dll files for communicating with instruments, such as ThorLabs instruments.
In these cases, a C-wrapper is used to access the functionality of the .dll files and custom drivers are
written. Our ThorLabs driver classes are currently under active development.

When you create an instance of a driver class, you may be required to enter the GPIB or VISA address and/or
serial number of your device as parameters. Read the docs for that particular instrument driver for details.

Upon creation of the driver class instrument, a connection to the instrument will be established. That's all
you need to do! Then you are free to use that driver's methods to set and read parameters on the instrument.

.. note::
    If you can't find a driver for your instrument, you should be able to connect to instruments from other 
    libraries as well and use it seamlessly with pyscan. 
    
    For further help, or for custom driver support, contact the developers by email (amounce@sandia.gov) or
    by creating an issue on github.

RunInfo
-------

A :class:`.RunInfo` class instance is where you will determine how the experiment will run. It will also be populated 
with more useful metadata about the experiment after the experiment has completed. RunInfo inherits from :class:`.ItemAttribute`
as well, so you can access its attribute just like a dictionary for convenience.

The essential components you must set on a RunInfo are **scans** and a **measure_function**.
A :class:`scan<.AbstractScan>` represents an independent variable that the experiment will iterate over.
You may set up to 4 scans, labeled as `scan0`, `scan1`, `scan2`, and `scan3`.

When the experiment is run, it will place the scans in a loop and iterate over the scan values. 
After each iteration, the experiment collects data using the **measure function**. This continues
until every combination of values has been exhausted.

Running the Experiment
----------------------

The experiment is run using one of two methods: :meth:`start_thread()<.AbstractExperiment.start_thread>` or :meth:`run()<.Experiment.run>`.

``start_thread()`` actually calls ``run()``. The only difference is that ``run()``
is a blocking method, so the console will freeze until the experiment is complete, while ``start_thread()`` 
calls ``run()`` in a new thread, so it is non-blocking. The ``start_thread()`` method is required in order to 
perform live-plotting.

Live Plots
----------

One extremely useful feature of pyscan is the built-in ability to monitor your data collection live. It can
either reassure you that the experiment is progressing as expected, or alert you that something is off. If
necessary, you can terminate the experiment using **CTRL+C**, modify the experiment parameters, and try again.

What's next?
------------

1. Continue to the Basic Example for a step-by-step walkthrough of how to setup and run an experiment.
2. Check out the Demo Notebooks for a variety of common examples.