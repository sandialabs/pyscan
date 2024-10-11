# -*- coding: utf-8 -*-
from PrincetonInstruments.LightField.AddIns import Pulse
from PrincetonInstruments.LightField.AddIns import ExperimentSettings
from PrincetonInstruments.LightField.AddIns import CameraSettings
from PrincetonInstruments.LightField.Automation import Automation
from ...general.item_attribute import ItemAttribute

import clr
import sys
import os
import spe_loader as sl
from time import sleep
from System.IO import print_speeds, Path
from System import String
from System.Collections.Generic import List

sys.path.append(os.environ['LIGHTFIELD_ROOT'])
sys.path.append(os.environ['LIGHTFIELD_ROOT'] + "\\AddInViews")
clr.AddReference('PrincetonInstruments.LightFieldViewV5')
clr.AddReference('PrincetonInstruments.LightField.AutomationV5')
clr.AddReference('PrincetonInstruments.LightFieldAddInSupportServices')


class PrincetonPiMax4(ItemAttribute):
    '''
    Class to control Princeton Instruments PI MAX 4 camera

    Methods
    -------
    print_device_information()
        Prints the model and serial number of the device
    get_settings()
        Returns the experimental settings

    '''

    def __init__(self, verbose=False):

        self.auto = Automation(True, List[String]())
        self.experiment = self.auto.LightFieldApplication.Experiment

        self.application = self.auto.LightFieldApplication
        self.file_manager = self.application.FileManager

        self.verbose = False
        self._version = "0.1.0"

    def print_device_information(self):
        print("Experiment Device Information:")
        # Print model and serial number of current device
        for device in self.experiment.ExperimentDevices:
            print(String.Format(
                '\t{0} {1}',
                device.Model,
                device.SerialNumber))

    def get_settings(self, setting):
        if self.experiment.Exists(setting):
            value = self.experiment.GetValue(setting)
            if self.verbose:
                print(String.Format(
                    '{0} {1} = {2}', "\tReading ",
                    str(setting),
                    value))
            return value

    def print_current_capabilities(self, setting):
        # Get current ADC rates that correspond
        # with the current quality setting
        print(String.Format(
            "{0} {1} {2}", "Current",
            setting, "Capabilities:"))

        for item in self.experiment.GetCurrentCapabilities(setting):
            print_speeds(item)

    def print_maximum_capabilities(self, setting):
        # Get Max Capabilities
        print(String.Format(
            "{0} {1} {2}", "Maximum",
            setting, "Capabilities:"))

        for item in self.experiment.GetMaximumCapabilities(setting):
            if (setting == CameraSettings.AdcSpeed):
                print_speeds(item)
            else:
                print(String.Format('\t{0} {1}', setting, item))

    def set_value(self, setting, value, verbose=False):
        # Check for existence before setting
        # gain, adc rate, or adc quality
        if self.experiment.Exists(setting):
            if self.verbose:
                print(String.Format(
                    "{0}{1} to {2}", "Setting ",
                    setting, value))

            self.experiment.SetValue(setting, value)

    @property
    def gating_mode(self):
        self._gating_mode = self.get_settings(CameraSettings.GatingMode, self.verbose)
        return self._gating_mode

    @gating_mode.setter
    def gating_mode(self, value):
        self.set_value(CameraSettings.GatingMode, value)
        self._gating_mode = value

    @property
    def gate_width(self):
        self._gate_width = self.get_settings(CameraSettings.GatingRepetitiveGate).Width / 1e6
        return self._gate_width

    @gate_width.setter
    def gate_width(self, new_value):
        new_value

        delay = self.get_settings(CameraSettings.GatingRepetitiveGate).Delay
        self.set_value(CameraSettings.GatingRepetitiveGate, Pulse(new_value, delay))
        self._gate_width = new_value

    @property
    def gate_delay(self):
        self._gate_delay = self.get_settings(CameraSettings.GatingRepetitiveGate).delay
        return self._gate_delay

    @gate_delay.setter
    def gate_delay(self, new_value):
        width = self.get_settings(CameraSettings.GatingRepetitiveGate).Width
        self.set_value(CameraSettings.GatingRepetitiveGate, Pulse(width, new_value))
        self._gate_delay = new_value

    @property
    def intensifier_gain(self):
        self._intensifier_gain = self.get_settings(CameraSettings.IntensifierEMIccdGain)
        return self._intensifier_gain

    @intensifier_gain.setter
    def intensifier_gain(self, new_value):
        self.set_value(CameraSettings.IntensifierEMIccdGain, int(new_value))
        self._intensifier_gain = new_value

    def acquire_image(self):
        self.save_file('temp')
        try:
            os.remove('c:/snl/lightfield/temp.spe')
            os.remove('c:/snl/lightfield/temp-raw.spe')

        except FileNotFoundError:
            pass

        self.experiment.Acquire()

        while True:
            try:
                with NoStdStreams():
                    image = sl.load_from_files(['c:/snl/lightfield/temp.spe']).data[0][0]
                break
            except PermissionError:
                sleep(0.05)
            except FileNotFoundError:
                sleep(0.05)

        return image

    def save_file(self, filename):
        # Set the base file name
        self.experiment.SetValue(
            ExperimentSettings.FileNameGenerationBaseFileName,
            Path.GetFileName(filename))

        # Option to Increment, set to false will not increment
        self.experiment.SetValue(
            ExperimentSettings.FileNameGenerationAttachIncrement,
            False)

        # Option to add date
        self.experiment.SetValue(
            ExperimentSettings.FileNameGenerationAttachDate,
            False)

        # Option to add time
        self.experiment.SetValue(
            ExperimentSettings.FileNameGenerationAttachTime,
            False)

    def stop(self):

        self.experiment.Stop()


class NoStdStreams(object):
    def __init__(self, stdout=None, stderr=None):
        self.devnull = open(os.devnull, 'w')
        self._stdout = stdout or self.devnull or sys.stdout
        self._stderr = stderr or self.devnull or sys.stderr

    def __enter__(self):
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush()
        self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush()
        self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        self.devnull.close()
