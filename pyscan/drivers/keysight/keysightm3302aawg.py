# -*- coding: utf-8 -*-
import keysightSD1
from ...general.item_attribute import ItemAttribute
import sys
sys.path.append(r'c:\Program Files (x86)\Keysight\SD1\Libraries\Python')


class KeysightM3302AAWG(ItemAttribute):
    '''Class to control Keysight M3302A PXIe AWG and Digitizer Combination

    Parameters
    ----------
    chassis : int
        The index of the chasis used
    slot : int
        The index of the card slot



    '''

    def __init__(self, chassis, slot):

        self.chassis = chassis
        self.slot = slot

        self._version = "0.1.0"

        self.module = keysightSD1.SD_AOU()
        self.module.openWithSlot("", self.chassis, self.slot)

    def set_channel_amplitude(self, channel, amplitude):

        self.module.channelAmplitude(channel, amplitude)

    def set_channel_wave_shape(self, channel, new_value):
        values = {'off': 0, 'sin': 1, 'tri': 2, 'squ': 4, 'dc': 5, 'awg': 6}
        if new_value in values:
            self.module.channelWaveShape(channel, values[new_value])
            self._wave_shape = new_value
        else:
            print('Wave shape must be off, sin, tri, squ, dc, or awg')

    def set_channel_trigger_config(self, channel, source=0, behavior=3):
        '''
        awg_index - index of wave form
        source - external: 0, PXI: 4000+value
        behavior - 1:Acvite high, 2: Active low, 3: rising edge, 4: falling edge
        '''
        self.module.AWGtriggerExternalConfig(
            channel, source, behavior, 0)

    def set_channel_awg_from_array(
            self, channel, trigger_mode, start_delay, cycles, prescalar, waveform_type,
            waveform_data_A, waveform_data_B=None, padding_mode=0):
        '''
        Parameters
        ----------
        channel
        trigger_mode : int
             6 play, then wait for trigger
        start_delay : float
        cycles : int
            0 = infinite
        prescalar : int
             0
        waveform_type : int
            0
        waveform_data_A : array
        '''

        self.module.AWGfromArray(
            channel, trigger_mode, start_delay, cycles,
            prescalar, waveform_type, waveform_data_A, waveform_data_B,
            padding_mode)

    def reset_channel_phase(self, channel):

        self.module.channelPhaseReset(channel)

    def flush_waveforms(self):
        self.module.waveformFlush()

    # def setup_cpmgxy8(self, pi2, delay, ncycles, trigger_channel=4000,
    #                   phase_lag=30):
    #     x, y, _ = make_cpmgxy8_arbs(pi2, delay, phase_lag)

    #     self.flush_waveforms()

    #     for i in range(2):
    #         self.set_channel_wave_shape(i+1, 'awg')
    #         self.set_channel_amplitude(i+1, 1)

    #     self.set_channel_awg_from_array(1, 6, 0, ncycles, 0, 0, x, padding_mode=0)
    #     self.set_channel_awg_from_array(2, 6, 0, ncycles, 0, 0, y, padding_mode=0)

    #     for i in range(2):
    #         self.reset_channel_phase(i+1)
    #         self.set_channel_trigger_config(i+1, trigger_channel, 3)

    # def setup_hahn_echo(self, pi2, delay, ncycles, delay1=None, trigger_channel=4000,
    #                     end_phase=0, phase_lag=30):
    #     x, y, _ = make_hahn_echo_arbs(pi2, delay,delay1=delay1, end_phase=end_phase, phase_lag=phase_lag)

    #     self.flush_waveforms()

    #     for i in range(2):
    #         self.set_channel_wave_shape(i+1, 'awg')
    #         self.set_channel_amplitude(i+1, 1)

    #     self.set_channel_awg_from_array(1, 6, 0, ncycles, 0, 0, x, padding_mode=0)
    #     self.set_channel_awg_from_array(2, 6, 0, ncycles, 0, 0, y, padding_mode=0)

    #     for i in range(2):
    #         self.reset_channel_phase(i+1)
    #         self.set_channel_trigger_config(i+1, trigger_channel, 3)

    # def setup_ramsey(self, pi2, delay, ncycles, trigger_channel=4000,
    #                     phase=90, phase_lag=50):
    #     x, y, _ = make_ramsey_phase_arbs(pi2, delay, phase, phase_lag)

    #     self.flush_waveforms()

    #     for i in range(2):
    #         self.set_channel_wave_shape(i+1, 'awg')
    #         self.set_channel_amplitude(i+1, 1)

    #     self.set_channel_awg_from_array(1, 6, 0, ncycles, 0, 0, x)
    #     self.set_channel_awg_from_array(2, 6, 0, ncycles, 0, 0, y)

    #     for i in range(2):
    #         self.reset_channel_phase(i+1)
    #         self.set_channel_trigger_config(i+1, trigger_channel, 3)
