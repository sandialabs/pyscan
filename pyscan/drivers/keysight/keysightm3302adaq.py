# -*- coding: utf-8 -*-
from ...general.item_attribute import ItemAttribute

import sys
sys.path.append(r'c:\Program Files (x86)\Keysight\SD1\Libraries\Python')

try:
    import keysightSD1
except:
    # print('Could not load Keysight SD1')
    pass


class KeysightM3302ADAQ(ItemAttribute):
    '''
    Class for controling the Keysight M3302A DAQ sub module

    Properties and fucntions are wrappers around keysight SDK

    Parameters
    ----------
    chassis : int
        chassis index
    slot : int
        slot of card
    channel : int
        channel of DAQ

    Attributes
    ----------
    (Properties)
    coupling :
        queries input coupling
        returns:
            0 - DC
            1 - AC
    full_scale :
        queries full scale of input voltage
        returns float
    impedance :
        queries input impedence
        returns:
            0 - high Z
            1 - 50 Ohms

    '''

    def __init__(self, chassis, slot, channel):

        self.chassis = chassis
        self.slot = slot
        self.channel = channel
        self._version = "0.1.0"

        self.module = keysightSD1.SD_AIN()
        self.module.openWithSlot("", self.chassis, self.slot)

    @property
    def coupling(self):
        self._coupling = self.module.channelCoupling(self.channel)
        return self._coupling

    @property
    def full_scale(self):
        self._full_Scale = self.module.channelFullScale(self.channel)
        return self._full_scale

    @property
    def impedance(self):
        self._impedance = self.module.channelImpedance(self.channel)
        return self._impedance

    def start(self):
        '''
        Starts DAQ acuqisition
        '''

        self.module.DAQstart(self.channel)

    def flush(self):
        '''
        Flushes memory of DAQ
        '''

        self.module.DAQflush(self.channel)

    def trigger(self):
        '''
        Manually triggers the DAQ
        '''

        self.module.DAQtrigger(self.channel)

    def close(self):
        '''
        Closes DAQ module
        '''

        self.module.close()

    def channel_input_config(self, full_scale, impedance, coupling):
        '''
        Configures the cannel inputs

        Args:
            full_scale - float volage input scale

            impedance - (int)
                options:
                0 - high Z
                1 - 50 Ohms

            coupling - (int)
                options:
                0 - DC
                1 - AC
        '''
        self.module.channelInputConfig(self.channel, full_scale, impedance, coupling)

    def channel_trigger_config(self, analog_trigger_mode, threshold):
        '''
        Configure how to trigger the channel

        Args:
            analog_trigger_mode options:
                1 - Rising Edge
                2 - Falling edge
                3 - Both

        Threshold options:
        voltage level (float)
        '''

        self.module.channelTriggerConfig(self.channel, analog_trigger_mode, threshold)

    def DAQ_config(self, points_per_cycle, ncycles,
                   trigger_delay, trigger_mode):
        '''
        points_per_cycle: int

        n_cycles: int

        trigger_delay: number of points to move the start int

        trigger_mode options:
        0 - Auto trigger
        1 - Software/HVI
        2 - External Digial Trigger
        3 - External Analog Trigger

        '''
        self.module.DAQconfig(self.channel,
                              points_per_cycle,
                              ncycles,
                              trigger_delay,
                              trigger_mode)

    def digital_trigger_config(self, source, behavior):
        '''
        source options:
        0 - external
        1 - pxi

        behavior options:
        1 - high level
        2 - low level
        3 - rising edge
        4 - falling edge
        '''
        self.module.DAQdigitalTriggerConfig(self.channel, source, behavior)

    def read_counter(self):
        return self.module.DAQcounterRead(self.channel)

    def read_data(self, points, timeout=5):
        return self.module.DAQread(self.channel, points, timeout)

    def external_trigger_mode(self, time, cycles, trigger_channel=0, behavior=3):
        n_points = int(time * 500e6)  # 500 MHz daq resolution
        self.channel_input_config(full_scale=0.250, impedance=1, coupling=0)
        self.channel_trigger_config(analog_trigger_mode=1, threshold=1)
        self.DAQ_config(points_per_cycle=n_points, ncycles=cycles,
                        trigger_delay=0, trigger_mode=2)
        self.digital_trigger_config(source=trigger_channel, behavior=behavior)
