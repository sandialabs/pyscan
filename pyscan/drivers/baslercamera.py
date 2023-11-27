# -*- coding: utf-8 -*-
"""
BaslerCamera
============
"""

from pyscan.general.itemattribute import ItemAttribute
from .pylonsdk import PylonSDK
from pypylon import pylon


class BaslerCamera(PylonSDK):
    '''
    Class to control Basler Cameras

    Parameters
    ----------
    None

    Yields
    ------
    Properties which can be get and set :
        gain : float
            sets/queries the camera gain in dB. Range: [0.0 , 24.0]
        width : int
            sets/queries the camera image width in pixels. Range: [4, 1928]
        height : int
            sets/queries the camera image height in pixels. Range: [1, 1208]
        pixel_format : str
            sets/queries the pixel depth/format. Values  ['Mono8', 'Mono12', 'Mono12p']
        exposure_time : float
            sets/queries the exposure_time. Range: [21.0, 10000000.0]
    Other properties : 
        max_buffer: int
            Range: [0, 4294967295]
        x_offset : int
            Range: [0, 1920]
        y_offset : int
            Range: [0, 1200]
        autogain : bool
            Autogain on or off
        autoexposure : bool
            Autoexposure on or off
        line_selector : str
            Values: ['Line1','Line2','Line3', 'Line4']
        line_inverter : bool
        trigger_delay : float
        trigger_source : str
            Values: ['Line1','Line2','Line3', 'Line4']
        trigger_selector : str
            Values: ['FrameStart', 'FrameBurstStart']
        trigger_activation : str
            Values: ['RisingEdge', 'FallingEdge']
        trigger_mode : str
            Values: ['Off', 'On']
        burst_frame_count : int
            Range: [1, 255]
        line_debouncer_time : float
            Range: [0.0, 2000.0]
        fps : 
            Readonly
        is_grabbing : 
            Readonly


    '''

    def __init__(self, default_config=True, verbose=False, debug=False):

        self.instrument = pylon.InstantCamera(
            pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.instrument.RegisterConfiguration(pylon.ConfigurationEventHandler(),pylon.RegistrationMode_ReplaceAll,pylon.Cleanup_Delete)

        self.verbose = verbose
        self.debug = debug

        self.open()

        self.initialize_properties()
        self.update_properties()

        if default_config:
            self.image_shape= [0, 0, 1920, 1200]
            self.pixel_format = 'Mono12'
            self.exposure_time = 6000
            self.gain = 0.0

    def initialize_properties(self):

        self.add_device_property({'name': 'max_buffer',
                                  'get_command': lambda: self.instrument.MaxNumBuffer.GetValue(),
                                  'return_type': int,
                                  'set_command': lambda x: self.instrument.MaxNumBuffer.SetValue(x),
                                  'int_range': [0, 4294967295]})

        self.add_device_property({'name':'x_offset',
                                  'get_command': lambda: self.instrument.OffsetX.GetValue(),
                                  'return_type': int,
                                  'set_command': lambda x: self.instrument.OffsetX.SetValue(x),
                                  'int_range': [0, 1920]})

        self.add_device_property({'name':'y_offset',
                                  'get_command': lambda: self.instrument.OffsetY.GetValue(),
                                  'return_type': int,
                                  'set_command': lambda x: self.instrument.OffsetY.SetValue(x),
                                  'int_range': [0, 1200]})

        self.add_device_property({'name':'width',
                                  'get_command': lambda: self.instrument.Width.GetValue(),
                                  'return_type': int,
                                  'set_command': lambda x: self.instrument.Width.SetValue(x),
                                  'int_range': [4, 1928]})

        self.add_device_property({'name':'height',
                                  'get_command': lambda: self.instrument.Height.GetValue(),
                                  'return_type': int,
                                  'set_command': lambda x: self.instrument.Height.SetValue(x),
                                  'int_range':[1, 1208]})

        self.add_device_property({'name':'autogain',
                                  'get_command': lambda: self.instrument.GainAuto.GetValue(),
                                  'return_type': bool,
                                  'set_command': lambda x: self.instrument.GainAuto.SetValue(x),
                                  'values':[True,False],
                                  'type':'boolonoff'})

        self.add_device_property({'name':'autoexposure',
                                  'get_command': lambda: self.instrument.ExposureAuto.GetValue(),
                                  'return_type': bool,
                                  'set_command': lambda x: self.instrument.ExposureAuto.SetValue(x),
                                  'values':[True,False],
                                  'type':'boolonoff'})

        self.add_device_property({'name': 'gain',
                                  'get_command': lambda: self.instrument.Gain.GetValue(),
                                  'return_type': float,
                                  'set_command': lambda x: self.instrument.Gain.SetValue(x),
                                  'range':[0.0, 24.0]})

        self.add_device_property({'name': 'exposure_time',
                                  'get_command': lambda: self.instrument.ExposureTime.GetValue(),
                                  'return_type': float,
                                  'set_command': lambda x: self.instrument.ExposureTime.SetValue(x),
                                  'range': [21.0, 10000000.0]})

        self.add_device_property({'name':'pixel_format',
                                  'get_command': lambda: self.instrument.PixelFormat.GetValue(),
                                  'return_type': str,
                                  'set_command': lambda x: self.instrument.PixelFormat.SetValue(x),
                                  'values': ['Mono8','Mono12','Mono12p']})

        self.add_device_property({'name':'line_selector',
                                  'get_command': lambda: self.instrument.LineSelector.GetValue(),
                                  'return_type': str,
                                  'set_command': lambda x: self.instrument.LineSelector.SetValue(x),
                                  'values': ['Line1','Line2','Line3', 'Line4']})

        self.add_device_property({'name':'line_mode',
                                  'get_command': lambda: self.instrument.LineMode.GetValue(),
                                  'return_type': str,
                                  'set_command': lambda x: self.instrument.LineMode.SetValue(x),
                                  'values': ['Output']})

        self.add_device_property({'name':'line_source',
                                  'get_command': lambda: self.instrument.LineSource.GetValue(),
                                  'return_type': str,
                                  'set_command': lambda x: self.instrument.LineSource.SetValue(x),
                                  'values': ['ExposureActive']})

        self.add_device_property({'name':'line_inverter',
                                  'get_command': lambda: self.instrument.LineInverter.GetValue(),
                                  'return_type': bool,
                                  'set_command': lambda x: self.instrument.LineInverter.SetValue(x),
                                  'values': [False, True]})

        self.add_device_property({'name': 'trigger_delay',
                                  'get_command': lambda: self.instrument.TriggerDelay.GetValue(),
                                  'return_type': float,
                                  'set_command': lambda x: self.instrument.TriggerDelay.SetValue(x),
                                  'values': [0.0, 1e6]})

        self.add_device_property({'name':'trigger_source',
                                  'get_command': lambda: self.instrument.TriggerSource.GetValue(),
                                  'return_type': str,
                                  'set_command': lambda x: self.instrument.TriggerSource.SetValue(x),
                                  'values': ['Line1', 'Line2', 'Line3', 'Line4']})

        self.add_device_property({'name':'trigger_selector',
                                  'get_command': lambda: self.instrument.TriggerSelector.GetValue(),
                                  'return_type': str,
                                  'set_command': lambda x: self.instrument.TriggerSelector.SetValue(x),
                                  'values': ['FrameStart', 'FrameBurstStart']})

        self.add_device_property({'name':'trigger_activation',
                                  'get_command': lambda: self.instrument.TriggerActivation.GetValue(),
                                  'return_type': str,
                                  'set_command': lambda x: self.instrument.TriggerActivation.SetValue(x),
                                  'values': ['RisingEdge', 'FallingEdge']})
        
        self.add_device_property({'name':'trigger_mode',
                                  'get_command': lambda: self.instrument.TriggerMode.GetValue(),
                                  'return_type': str,
                                  'set_command': lambda x: self.instrument.TriggerMode.SetValue(x),
                                  'values': ['Off', 'On']})

        self.add_device_property({'name':'burst_frame_count',
                                  'get_command': lambda: self.instrument.AcquisitionBurstFrameCount.GetValue(),
                                  'return_type': int,
                                  'set_command': lambda x: self.instrument.AcquisitionBurstFrameCount.SetValue(x),
                                  'range': [1, 255]})

        self.add_device_property({'name':'line_debouncer_time',
                                  'get_command': lambda: self.instrument.LineDebouncerTime.GetValue(),
                                  'return_type': float,
                                  'set_command': lambda x: self.instrument.LineDebouncerTime.SetValue(x),
                                  'range': [0.0, 2000.0]})


        self.update_properties()

    def update_properties(self):
        for q in ['x_offset', 'y_offset', 'width', 'height','autoexposure', 'autogain',
                  'exposure_time', 'pixel_format']:

            _ = self[q]

    @property
    def fps(self):
        return self.instrument.ResultingFrameRate()
    
    @property
    def is_grabbing(self):
        return self.instrument.IsGrabbing()

    def start_grabbing_max(self, n):
        return self.instrument.StartGrabbingMax(n)

    def open(self):
        self.instrument.Open()

    def close(self):
        self.instrument.Close()

    def get_one_frame(self):

        self.grab(1)

        return self.get_frame()

    def retrieve_results(self, timeout=60240):
        return self.instrument.RetriveResults(timeout, pylon.TimeoutHandling_ThrowException)

    def wait_for_frametrigger_ready(self,timeout):
        self.instrument.WaitForFrameTriggerReady(timeout,pylon.TimeoutHandling.ThrowException)

    def trigger(self):
        '''
        Executes software trigger

        Args: None

        returns float
    
        '''
        self.instrument.ExecuteSoftwareTrigger()

    def continuous_images(self):
        
        self.trigger_selector = 'FrameStart'
        self.trigger_mode = 'Off'
        
        self.trigger_selector = 'FrameBurstStart'
        self.trigger_mode = 'Off'

    def continuous_external_trigger_mode(self, trigger_source=3):

        self.trigger_selector = 'FrameStart'
        self.trigger_mode = 'On'
        self.trigger_source = 'Line{}'.format(trigger_source)
        self.line_debouncer_time = 10.0
        
    def continuous_external_burst_mode(self, frames_per_burst, 
                                       trigger_source=3,
                                       burst_source=4):
        
        self.trigger_selector = 'FrameStart'
        self.trigger_mode = 'On'
        self.trigger_source = 'Line{}'.format(trigger_source)
        self.line_debouncer_time = 10.0
        
        self.trigger_selector = 'FrameBurstStart'
        self.trigger_mode = 'On'
        self.trigger_source = 'Line{}'.format(burst_source)
        self.burst_frame_count = frames_per_burst
        self.line_debouncer_time = 10.0


    def __del__(self):
        self.close()
