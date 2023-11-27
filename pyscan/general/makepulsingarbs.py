# -*- coding: utf-8 -*-
"""
Make Pulsing Arbs
=================
"""


import numpy as np


def make_rabi_arbs(
    pi2, sample_rate, 
    phase_lag=20, 
    off_time=100):

    '''Makes arbitrary waveforms for a rabi pulse sequence. Order of sequence is [`phase_lag`, `pi2`, `off_time`].

    :param pi2: pi/2 pulse time in ns.
    :type pi2: int
    :param sample_rate: Sample rate of awg in Hz.
    :type sample_rate: int
    :param phase_lag: Time in ns for pi/2 phase to be setup, defaults to
    :type phase_lag: int, optional
    :param off_time: Time in ns of off time after pi2, defaults to 100.
    :type off_time: int, optional
    :returns:
        (tuple): tuple containing:
            - x_channel (`array(int)`) - arb to be uploaded for x channel
            - y_channel (`array(int)`) - arb to be uploaded for y channel
            - mw (`array(int)`) - arb indicating when mw is on, used to plot the pulse sequence

    '''

    pi2 = int(pi2*(sample_rate*1e-9)) # pi2 * sample rate in ns
    phase_lag = int(phase_lag*(sample_rate*1e-9)) # phase lag * sample rate in ns
    
    x_channel = []
    y_channel = []
    mw = []

    # Initialize
    x_channel += [1 for i in range(pi2+phase_lag)]
    y_channel += [0 for i in range(pi2+phase_lag)]
    mw += [0 for i in range(phase_lag)]
    mw += [1 for i in range(pi2)]

    x_channel += [0 for i in range(off_time)]
    y_channel += [0 for i in range(off_time)]
    mw += [0 for i in range(off_time)]

    mw = np.array(mw)
    x_channel = np.array(x_channel)
    y_channel = np.array(y_channel)

    return x_channel, y_channel, mw

def make_ramsey_phase_arbs(
    delay, pi2, pi2_offset, sample_rate, end_phase,
    phase_lag=20,
    off_time=100):

    '''Makes arbitrary waveforms for a ramsay pulse sequence. Sequence order is [`phase_lag`, `pi2_offset` + `pi2`, `delay`, `pi2_offset` + `pi2`, `off_time`].

    :param delay: Delay between pi/2 pulses in ns.
    :type delay: float
    :param pi2: pi/2 time in ns.
    :type pi2: float
    :param pi2_offset: Extra time for pi pulses to activate.
    :type pi2_offset: float
    :param sample_rate: Sample rate of awg in Hz
    :type sample_rate: int
    :param end_phase: Phase of projection pulse in degrees.
    :type end_phase: float
    :param phase_lag: Time in ns for pi/2 phase to be setup, defaults to 20.
    :type phase_lag: float, optional
    :param off_time: Time in ns of off time after second pi2 phase, defaults to 100.
    :type off_time: int, optional
    :returns:
        (tuple): tuple containing:
            - x_channel (`array(int)`) - arb to be uploaded for x channel
            - y_channel (`array(int)`) - arb to be uploaded for y channel
            - mw (`array(int)`) - arb indicating when mw is on, used to plot the pulse sequence

    '''

    pi2 = int(pi2*(sample_rate*1e-9))
    pi2_offset = int(pi2_offset*(sample_rate*1e-9))
    delay = int(delay*(sample_rate*1e-9))
    
    pi2 += pi2_offset

    x_channel = []
    y_channel = []
    mw = []

    # Tip
    x_channel += [1 for i in range(pi2+phase_lag)]
    y_channel += [0 for i in range(pi2+phase_lag)]
    mw += [0 for i in range(phase_lag)]
    mw += [1 for i in range(pi2)]
    # Delay and project
    x_channel += [np.cos(end_phase*np.pi/180) for i in range(delay+pi2)]
    y_channel += [np.sin(end_phase*np.pi/180) for i in range(delay+pi2)]
    mw += [0 for i in range(delay)]
    mw += [1 for i in range(pi2)]
    # Off
    x_channel += [0 for i in range(off_time)]
    y_channel += [0 for i in range(off_time)]
    mw += [0 for i in range(off_time)]

    mw = np.array(mw)
    x_channel = np.array(x_channel)
    y_channel = np.array(y_channel)

    return x_channel, y_channel, mw


def make_hahn_echo_arbs(
    delay, pi2, pi2_offset, sample_rate,
    end_phase=0, 
    phase_lag=0,
    off_time=100):

    '''
    Makes arbitrary waveforms for a hahn echo pulse sequence. Sequence order is [`phase_lag`, `pi2_offset` + `pi2`, `delay`, `pi2_offset` + `pi`, `delay`, `pi2_offset` + `pi3/2`].

    :param delay: Delay in ns between pi pulses.
    :type delay: float
    :param pi2: pi/2 time in ns.
    :type pi2: float
    :param pi2_offset: Extra time for pi pulses to activate.
    :type pi2_offset: float
    :param sample_rate: Sample rate of awg in Hz
    :type sample_rate: int
    :param end_phase: Phase of projection pulse in degrees for pi3/2 phase, defaults to 0.
    :type end_phase: float, optional
    :param phase_lag: Time in ns for pi/2 phase to be setup, defaults to 0.
    :type phase_lag: float, optional
    :param off_time: Time in ns of off time after pi pulses, defaults to 100.
    :type off_time: int, optional
    :returns:
        (tuple): tuple containing:
            - x (`array(int)`) - arb to be uploaded for x channel
            - y (`array(int)`) - arb to be uploaded for y channel
            - mw (`array(int)`) - arb indicating when mw is on, used to plot the pulse sequence

    '''
 
    pi2 = int(pi2*(sample_rate*1e-9))
    pi2_offset = int(pi2_offset*(sample_rate*1e-9))
    pi = 2*pi2 + pi2_offset
    pi32 = 3*pi2 + pi2_offset
    pi2 += pi2_offset

    delay = int(delay*(sample_rate*1e-9))

    x_channel = []
    y_channel = []
    mw = []

    # Tip
    x_channel += [1 for i in range(pi2 + phase_lag)]
    y_channel += [0 for i in range(pi2 + phase_lag)]
    mw += [0 for i in range(phase_lag)]
    mw += [1 for i in range(pi2)]
    # pi pulse
    x_channel += [1 for i in range(pi + delay)]
    y_channel += [0 for i in range(pi + delay)]
    mw += [0 for i in range(delay)]
    mw += [1 for i in range(pi)]
    # Delay and project
    x_channel += [np.cos(end_phase*np.pi/180) for i in range(delay+pi32)]
    y_channel += [np.sin(end_phase*np.pi/180) for i in range(delay+pi32)]
    mw += [0 for i in range(delay)]
    mw += [1 for i in range(pi32)]
    # End phase
    x_channel += [1 for i in range(off_time)]
    y_channel += [0 for i in range(off_time)]
    mw += [0 for i in range(off_time)]

    mw = np.array(mw)
    x_channel = np.array(x_channel)
    y_channel = np.array(y_channel)

    return x_channel, y_channel, mw

def make_cpmgxy8n_arbs(
    delay, pi2, pi, nxy8, sample_rate,
    end_phase=0, 
    phase_lag=2,
    off_time=100):
    
    '''
    Makes arbitrary waveforms for a cpmgxy8-n pulse sequence. 

    :param delay: Time in ns between pi pulses.
    :type delay: float
    :param pi2: pi/2 time in ns.
    :type pi2: float
    :param sample_rate: Sample rate of awg in Hz
    :type sample_rate: int
    :param phase_lag: Time in ns for pi/2 phase to be setup, defaults to 2.
    :type phase_lag: float
    :param off_time: Time in ns of off time after pi pulses, defaults to 100.
    :type off_time: int, optional
    :returns:
        (tuple): tuple containing:
            - x (array(int)) - arb to be uploaded for x channel
            - y (array(int)) - arb to be uploaded for y channel
            - mw (array(int)) - arb indicating when mw is on, used to plot the pulse sequence
    '''

    pi2 = int(pi2*(sample_rate*1e-9))
    pi2_offset = int(pi2_offset*(sample_rate*1e-9))
    pi = 2*pi2 + pi2_offset
    pi32 = 3*pi2 + pi2_offset
    pi2 += pi2_offset

    delay = int(delay*(sample_rate*1e-9))

    x_channel = []
    y_channel = []
    mw = []

    if delay % 2 != 0:
        delays = self.make_quantum_interpolation_delays(
            self.sample_rate, delay, nxy8)
    else:
        delays = [delay for i in range(2 * 16 * nxy8 + 1)]

    x_phases = []
    y_phases = []
    for i in range(nxy8):
        x_phases += [1, 0, 1, 0, 0, 1, 0, 1]
        y_phases += [0, 1, 0, 1, 1, 0, 1, 0]
    x_phases += [np.cos(end_phase*np.pi/180)]
    y_phases += [np.sin(end_phase*np.pi/180)]

    x_channel = []
    y_channel = []
    mw_channel = []
    
    # Initialize
    x_channel += [1 for i in range(pi2+phase_lag)]
    y_channel += [0 for i in range(pi2+phase_lag)]
    mw_channel += [0 for i in range(phase_lag)]
    mw_channel += [1 for i in range(pi2)]

    x, y, mw_channel = make_cpmgxy8n_pulse_arbs(pi, delays)
    x_channel += x
    y_channel += y
    mw_channel += mw

    # Project
    mw_channel += [1 for i in range((pi2*3))]
    x_channel += [np.cos(end_phase*np.pi/180) for i in range((pi2*3))]
    y_channel += [np.sin(end_phase*np.pi/180) for i in range((pi2*3))]

    mw_channel+=[0 for i in range(off_time)]
    x_channel += [1 for i in range(off_time)]
    y_channel += [0 for i in range(off_time)]

    mw_channel = np.array(mw_channel)
    x_channel = np.array(x_channel)
    y_channel = np.array(y_channel)

    return x_channel, y_channel, mw_channel


def make_cpmgxy8_corr_arbs(
    pi2, pi, delay, corr_time, nxy8, sample_rate, 
    end_phase=0,
    phase_lag=2,
    off_time=100):
    
    '''
    description

    '''

    pi2 = int(pi2*(sample_rate*1e-9))
    delay = int(delay*(sample_rate*1e-9))
    phase_lag = int(phase_lag*(sample_rate*1e-9))

    if delay % 2 != 0:
        delays = self.make_quantum_interpolation_delays(
            self.sample_rate, delay, nxy8)
    else:
        delays = [delay for i in range(2 * 16 * nxy8 + 1)]

    x_phases = []
    y_phases = []
    for i in range(nxy8):
        x_phases += [1, 0, 1, 0, 0, 1, 0, 1]
        y_phases += [0, 1, 0, 1, 1, 0, 1, 0]
    x_phases += [np.cos(end_phase*np.pi/180)]
    y_phases += [np.sin(end_phase*np.pi/180)]

    x_channel = []
    y_channel = []
    mw_channel = []
    
    # Tip
    x_channel += [1 for i in range(pi2+phase_lag)]
    y_channel += [0 for i in range(pi2+phase_lag)]
    mw_channel += [0 for i in range(phase_lag)]
    mw_channel += [1 for i in range(pi2)]

    # First CPMGXY8-N
    x, y, mw_channel = make_cpmgxy8n_pulse_arbs(pi, delays, x_phases, y_phases)
    x_channel += x
    y_channel += y
    mw_channel += mw

    # Project
    x_channel += [0 for i in range((pi2))]
    y_channel += [1 for i in range((pi2))]
    mw_channel += [1 for i in range((pi2))]

    # Correlate
    x_channel += [1 for i in range((pi2))]
    y_channel += [0 for i in range((pi2))]
    mw_channel += [0 for i in range((pi2))]

    # Tip
    x_channel += [1 for i in range(pi2)]
    y_channel += [0 for i in range(pi2)]
    mw_channel += [1 for i in range(pi2)]

    # Second CPMGXY8-N
    x, y, mw_channel = make_cpmgxy8n_pulse_arbs(pi, delays,  x_phases, y_phases)
    x_channel += x
    y_channel += y
    mw_channel += mw

    # Readout 
    x_channel += [0 for i in range((pi2*3))]
    y_channel += [1 for i in range((pi2*3))]
    mw_channel += [0 for i in range((pi2*3))]

    # End
    mw_channel+=[0 for i in range(off_time)]
    x_channel += [1 for i in range(off_time)]
    y_channel += [0 for i in range(off_time)]

    mw_channel = np.array(mw_channel)
    x_channel = np.array(x_channel)
    y_channel = np.array(y_channel)

    return x_channel, y_channel, mw_channel


def make_cpmgxy16n_arbs(
    pi2, pi, delay, nxy16, sample_rate,
    end_phase=0, 
    phase_lag=2):
    
    '''
    Makes arbitrary waveforms for a cpmgxy16-n pulse sequences

    Inputs:
        pi2(int) pi2 time in ns
        sample_rate(int) sample rate of awg in Hz
        phase_lab(int) time in ns for phase to be setup
        off_time

    returns:
        x (array(int)) - arb to be uploaded for x channel
        y (array(int)) - arb to be uploaded for y channel
        mw (array(int)) - arb indicating when mw is on, used to plot
        the pulse sequence

    '''

    pi2 = int(pi2*(sample_rate*1e-9))
    delay = int(delay*(sample_rate*1e-9))
    phase_lag = int(phase_lag*(sample_rate*1e-9))

    if delay % 2 != 0:
        delays = self.make_quantum_interpolation_delays(
            self.sample_rate, delay, nxy16)
    else:
        delays = [delay for i in range(2 * 16 * nxy16 + 1)]

    x_phases = []
    y_phases = []
    for i in range(nxy16):
        x_phases += [1, 0, 1, 0, 0, 1, 0, 1, -1, 0, -1, 0, 0, -1, 0, -1]
        y_phases += [0, 1, 0, 1, 1, 0, 1, 0, 0, -1, 0, -1, -1, 0, -1, 0]
    x_phases += [np.cos(end_phase*np.pi/180)]
    y_phases += [np.sin(end_phase*np.pi/180)]

    x_channel = []
    y_channel = []
    mw_channel = []
    
    # Tip
    x_channel += [1 for i in range(pi2+phase_lag)]
    y_channel += [0 for i in range(pi2+phase_lag)]
    mw_channel += [0 for i in range(phase_lag)]
    mw_channel += [1 for i in range(pi2)]
    
    # Make cpmgxy16n pulses 
    x, y, mw_channel = make_cpmgxy_pulse_arbs(pi, delays)
    x_channel += x
    y_channel += y
    mw_channel += mw

    # Project
    mw_channel += [1 for i in range((pi2*3))]
    x_channel += [np.cos(end_phase*np.pi/180) for i in range((pi2*3))]
    y_channel += [np.sin(end_phase*np.pi/180) for i in range((pi2*3))]

    # Off/End
    mw_channel+=[0 for i in range(off_time)]
    x_channel += [1 for i in range(off_time)]
    y_channel += [0 for i in range(off_time)]

    mw_channel = np.array(mw_channel)
    x_channel = np.array(x_channel)
    y_channel = np.array(y_channel)

    return x_channel, y_channel, mw_channel


def make_cpmgxy16_corr_arbs(
    pi2, pi, delay, corr_time, nxy16, sample_rate, 
    end_phase=0,
    phase_lag=2,
    off_time=100):
    
    '''
    Description

    '''

    pi2 = int(pi2*(sample_rate*1e-9))
    delay = int(delay*(sample_rate*1e-9))
    phase_lag = int(phase_lag*(sample_rate*1e-9))

    if delay % 2 != 0:
        delays = self.make_quantum_interpolation_delays(
            self.sample_rate, delay, nxy8)
    else:
        delays = [delay for i in range(2 * 16 * nxy8 + 1)]

    x_phases = []
    y_phases = []
    for i in range(nxy8):
        x_phases += [1, 0, 1, 0, 0, 1, 0, 1, -1, 0, -1, 0, 0, -1, 0, -1]
        y_phases += [0, 1, 0, 1, 1, 0, 1, 0, 0, -1, 0, -1, -1, 0, -1, 0]
    x_phases += [np.cos(end_phase*np.pi/180)]
    y_phases += [np.sin(end_phase*np.pi/180)]

    x_channel = []
    y_channel = []
    mw_channel = []
    
    # Tip
    x_channel += [1 for i in range(pi2+phase_lag)]
    y_channel += [0 for i in range(pi2+phase_lag)]
    mw_channel += [0 for i in range(phase_lag)]
    mw_channel += [1 for i in range(pi2)]

    # First CPMGXY8-N
    x, y, mw_channel = make_cpmgxy_pulse_arbs(pi, delays, x_phases, y_phases)
    x_channel += x
    y_channel += y
    mw_channel += mw

    # Project
    x_channel += [0 for i in range((pi2))]
    y_channel += [1 for i in range((pi2))]
    mw_channel += [1 for i in range((pi2))]

    # Correlate
    x_channel += [1 for i in range((pi2))]
    y_channel += [0 for i in range((pi2))]
    mw_channel += [0 for i in range((pi2))]

    # Tip
    x_channel += [1 for i in range(pi2)]
    y_channel += [0 for i in range(pi2)]
    mw_channel += [1 for i in range(pi2)]

    # Second CPMGXY8-N
    x, y, mw_channel = make_cpmgxy_pulse_arbs(pi, delays,  x_phases, y_phases)
    x_channel += x
    y_channel += y
    mw_channel += mw

    # Readout 
    x_channel += [0 for i in range((pi2*3))]
    y_channel += [1 for i in range((pi2*3))]
    mw_channel += [0 for i in range((pi2*3))]

    # End
    mw_channel+=[0 for i in range(off_time)]
    x_channel += [1 for i in range(off_time)]
    y_channel += [0 for i in range(off_time)]

    mw_channel = np.array(mw_channel)
    x_channel = np.array(x_channel)
    y_channel = np.array(y_channel)

    return x_channel, y_channel, mw_channel


def make_cpmgxy_pulse_arbs(pi, delays, x_phases, y_phases):

    x = []
    y = []
    mw = []

    for i in range(len(delays)//2 - 1):
        x += [x_phases[i] for i in range(delay[2*i])]
        x += [x_phases[i] for i in range(pi)]
        x += [x_phases[i+1] for i in range(delay[2*i+1])]

        y += [y_phases[i] for i in range(delay[2*i])]
        y += [y_phases[i] for i in range(pi)]
        y += [y_phases[i+1] for i in range(delay[2*i+1])]

        mw += [0 for i in range(delay[2*i])]
        mw += [1 for i in range(pi)]
        mw += [0 for i in range(delay[2*i+1])]

    return x, y, mw
