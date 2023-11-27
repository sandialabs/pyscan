# -*- coding: utf-8 -*-
"""
Setup Widefield CWODMR
======================
"""

import sys,time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pypylon import pylon
from IPython import display
from matplotlib.backends.backend_agg import FigureCanvasAgg as fc

import pyscan as ps


def widefield_cleanup(expt):
    expt.devices.mw.output = 0

def measure_image(self, expt):
    """
    Take images in chunks (suggested: 500) for live plots/systematic error.
    """
    d = ps.ItemAttribute()
    
    runinfo = expt.runinfo
    devices = expt.devices

    imgavg = np.zeros((2, *devices.camera.image_shape[::-1]))
    d.imgs = np.zeros(devices.camera.image_shape[:2][::-1])
    tempimg = np.zeros(devices.camera.image_shape[:2][::-1])
    j = 0

    badrun = False

    while j < 2 * self.runinfo.n_averages:

        tempimg = self.devices.camera.get_frame(timeout = self.runinfo.timeout)

        if tempimg:

            img_buffer[j % 2] = tempimg
            if j % 2 == 1:
                if not badrun and np.all(img_buffer[1] != 0):
                    d.imgs += img_buffer[0] / img_buffer[1]
                else:
                    badrun = False
            j += 1
        else:
            badrun = True
    d.imgavg /= self.runinfo.n_averages

    return d

def setup_widefield_cwodmr(devices, n_averages, 
                           camera_exposure_time, camera_gain, camera_image_size,
                           camera_pixel_format, 
                           mw_amplitude, mw_settling_time, padding_time,
                           magnet_on, magnet_currents, magnet_voltages, n_repeats=None):
        
    if not all([q in devices.keys() for q in ['pb', 'mw','camera']]):
        print("Devices must be named 'pb', 'mw', and 'camera'.")

    # Setup instruments

    # Setup Camera
    if camera_image_size is not None:
        devices.camera.camera_image_size = camera_image_size
    devices.camera.pixel_format = camera_pixel_format
    devices.camera.gain = camera_gain
    devices.camera.exposure_time = camera_exosure_time

    # Setup Mw
    devices.mw.amplitude = 1
    devices.mw.output = 1

    # What is this?
    if False:
        cam.configure_trigger_line('Line3','FallingEdge',burst=True,burst_frames=2*self.runinfo.n_avgs)

    devices.camera.configure_output_line('Line4', 'ExposureActive', invert=True)
    devices.camera.configure_trigger_line('Line3', 'FallingEdge', burst=False)

    devices.camera.start_grabbing(2 * n_averages)
 
    # Setup pulse blaster
    camera_frame_period = 1e3 / devices.camera.fps
    devices.pb.setup_widefield_cwodmr(camera_frame_period, n_averages)

    # Setup Magnet
    if magnet_on:
        devices.magnet.currents = magnet_currents
        devices.magnet.voltages = magnet_voltages
        devices.magnet.output = magnet_on

    # Make runinfo
    runinfo = ps.RunInfo()

    runinfo.end_function = cleanup
    runinfo.measure_function = measure_image
    runinfo.n_averages = n_averages

    time.sleep(1) # to allow magnet to initialize so we can read correct values.

    return runinfo

