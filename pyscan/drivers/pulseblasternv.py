# -*- coding: utf-8 -*-
"""
NVPulseBlaster
==============
"""

from .pulseblaster import PulseBlaster
import numpy as np
def enum(**enums):
    return type('Enum', (), enums)

ns = 1
us = 1e3
ms = 1e6
s = 1e9

Inst = enum(
    CONTINUE=0,
    STOP=1,
    LOOP=2,
    END_LOOP=3,
    JSR=4,
    RTS=5,
    BRANCH=6,
    LONG_DELAY=7,
    WAIT=8,
    RTI=9
)

class NVPulseBlaster(PulseBlaster):

    def __init__(self, sample_rate=500e6):

        super().__init__()

        self.sample_rate = sample_rate
        self.awg_lag = 4

    def setup_lockin_fluor(self, sample_rate):
        '''
        Shutters microwaves on and off at frequency 2x
        samle rate
        
        Required pb channels: pb.mw, (optional pb.aom)   

        inputs:
            sample_rate - Frequency in Hz to turn mw on and off

        '''
        mw = 2 ** self.mw

        if hasattr(self, 'aom'):
            aom = 2**self.aom
        else:
            aom = 0

        sample_time = int(1/sample_rate*1e9//2)

        self.start_programming()
        self.inst(mw + aom, Inst.CONTINUE, 0, sample_time)
        self.inst(0, Inst.BRANCH, 0, sample_time)
        self.stop_programming()

        self.reset()
        self.start()

    def setup_lockin_cwodmr(self, sample_rate):
        '''
        Shutters microwaves on and off at frequency 2x
        samle rate
        
        Required pb channels: pb.mw, (optional pb.aom)   

        inputs:
            sample_rate - Frequency in Hz to turn mw on and off

        '''
        mw = 2 ** self.mw

        if hasattr(self, 'aom'):
            aom = 2**self.aom
        else:
            aom = 0

        sample_time = int(1/sample_rate*1e9//2)

        self.start_programming()
        self.inst(mw + aom, Inst.CONTINUE, 0, sample_time)
        self.inst(aom, Inst.BRANCH, 0, sample_time)
        self.stop_programming()

        self.reset()
        self.start()

    def setup_basler_trigger_single_frame(self, frame_rate):
        '''
        Triggers Basler camera in single trigger mode for one frame at a time
        
        Required pb channels: mw, camera_trigger


        Inputs:
            frame_rate in Hz
        
        '''
        
        period = 1/frame_rate*1e9
        if period%2 == 1:
            period += 1

        trigger_camera = 2**self.camera_trigger

        self.start_programming()
        self.inst(trigger_camera, Inst.CONTINUE, 0, period)
        self.inst(0, Inst.BRANCH, 0, period)
        self.stop_programming()

        self.reset()
        self.start()

    def setup_basler_two_burst_mw(self, period):
        '''
        Triggers the basler camera once for burst mode, then two triggers
        for mw on and mw off frames

        Required pb channels: mw, camera_trigger, camera_burst

        Inputs:
            frame_rate in Hz

        Returns:
            None

        '''
        
        period = period*1e9
        if period%2 == 1:
            period += 1


        mw_on = 2**self.mw
        trigger_camera = 2**self.camera_trigger
        burst_on = 2**self.camera_burst
        
        self.start_programming()
        self.inst(burst_on + mw_on, Inst.CONTINUE, 0, mw_settle_time)
        self.inst(trigger_camera + mw_on, Inst.CONTINUE, 0, period)
        self.inst(0, Inst.CONTINUE, 0, mw_settle_time)
        self.inst(trigger_camera, Inst.BRANCH, 0, period)
        self.stop_programming()

        self.reset()
        self.start()



    def setup_rabi(self, pi2, n_reps,
                   pi2_offset=0,
                   off_time=500,
                   init_time=15000,
                   readout_buffer=2000):
        '''     
        Performs single mw pulse and readout for NV pi/2 and
        pi calibration using switches for phase control

        Required pb channels: phase1, phase2, aom, daq, mw

        inputs:
            pi2 - pi2 time in ns
            n_reps - number of on/ref repeats
            off_time - time between on/off in ns
            init_time - aom initialization time in ns
        returns:
            (float) time in (s) for one 'repeition' which is one
            signal or reference

        Sequence:
        
        aom - init_time
        I - phase_lag
        mw+I - pi2
        0 - readout_buffer
        aom + daq - init_time
        0 - off time

        aom - init_time
        0 - phase_lag
        0 - pi2
        0 - readout_buffer
        aom + daq - init_time
        0 - off time

        '''

        if self.phase_control == 'switches':
            I = 0
            Q = 2**self.phase1
            nQ = 2**self.phase2
            nI = 2**self.phase1
            nI += 2**self.phase2

            awg = 0
            awg_lag = 2
        elif self.phase_control =='awg':
            I = 0
            Q = 0
            nQ = 0
            nI = 0

            awg = 2** self.awg
            awg_lag = self.awg_lag

        mw = 2**self.mw
        aom = 2**self.aom
        daq = 2**self.daq

        if pi2 == 0:
            mw = 0

        n_reps = n_reps//2

        pi2 += pi2_offset

        self.start_programming()
        self.inst(0, Inst.LOOP, n_reps, 100)
        self.inst(awg, Inst.CONTINUE, 0, awg_lag)
        # Pulse
        self.inst(aom + nI, Inst.CONTINUE, 0, init_time)
        self.inst(mw + nI, Inst.CONTINUE, 0, pi2)
        self.inst(nI, Inst.CONTINUE, 0, readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.CONTINUE, 0, off_time)
        # Reference
        self.inst(aom+ nI, Inst.CONTINUE, 0, init_time)
        self.inst(0+ nI, Inst.CONTINUE, 0, pi2)
        self.inst(0+ nI, Inst.CONTINUE, 0, readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.END_LOOP, 0, off_time)
        # End
        self.inst(0, Inst.STOP, 0, 100)
        self.stop_programming()

        rep_time = (init_time + pi2 + readout_buffer + init_time + off_time)

        return rep_time / 1e9
    def setup_rabi_mw2(self, pi2, n_reps,
                   pi2_offset=0,
                   off_time=500,
                   init_time=15000,
                   readout_buffer=2000):
        '''     
        Performs single mw pulse and readout for NV pi/2 and
        pi calibration using switches for phase control

        Required pb channels: phase1, phase2, aom, daq, mw

        inputs:
            pi2 - pi2 time in ns
            n_reps - number of on/ref repeats
            off_time - time between on/off in ns
            init_time - aom initialization time in ns
        returns:
            (float) time in (s) for one 'repeition' which is one
            signal or reference

        Sequence:
        
        aom - init_time
        I - phase_lag
        mw+I - pi2
        0 - readout_buffer
        aom + daq - init_time
        0 - off time

        aom - init_time
        0 - phase_lag
        0 - pi2
        0 - readout_buffer
        aom + daq - init_time
        0 - off time

        '''

        if self.phase_control == 'switches':
            I = 0
            Q = 2**self.phase1
            nQ = 2**self.phase2
            nI = 2**self.phase1
            nI += 2**self.phase2

            awg = 0
            awg_lag = 2
        elif self.phase_control =='awg':
            I = 0
            Q = 0
            nQ = 0
            nI = 0

            awg = 2** self.awg
            awg_lag = self.awg_lag

        mw = 2**self.mw
        mw2 = 2**self.mw2
        aom = 2**self.aom
        daq = 2**self.daq

        if pi2 == 0:
            mw = 0

        n_reps = n_reps//2

        pi2 += pi2_offset

        self.start_programming()
        self.inst(0, Inst.LOOP, n_reps, 100)
        self.inst(awg, Inst.CONTINUE, 0, awg_lag)
        # Pulse
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(mw2 + I, Inst.CONTINUE, 0, pi2)
        self.inst(I, Inst.CONTINUE, 0, readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.CONTINUE, 0, off_time)
        # Reference
        self.inst(aom, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.CONTINUE, 0, pi2)
        self.inst(0, Inst.CONTINUE, 0, readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.END_LOOP, 0, off_time)
        # End
        self.inst(0, Inst.STOP, 0, 100)
        self.stop_programming()

        rep_time = (init_time + pi2 + readout_buffer + init_time + off_time)

        return rep_time / 1e9    
    def setup_rabi_scope(self, pi2, n_reps,
                   pi2_offset=0,
                   off_time=500,
                   init_time=15000,
                   readout_buffer=2000):
        '''     
        Performs single mw pulse and readout for NV pi/2 and
        pi calibration using switches for phase control

        Required pb channels: phase1, phase2, aom, daq, mw

        inputs:
            pi2 - pi2 time in ns
            n_reps - number of on/ref repeats
            off_time - time between on/off in ns
            init_time - aom initialization time in ns
        returns:
            (float) time in (s) for one 'repeition' which is one
            signal or reference

        Sequence:
        
        aom - init_time
        I - phase_lag
        mw+I - pi2
        0 - readout_buffer
        aom + daq - init_time
        0 - off time

        aom - init_time
        0 - phase_lag
        0 - pi2
        0 - readout_buffer
        aom + daq - init_time
        0 - off time

        '''

        if self.phase_control == 'switches':
            I = 0
            Q = 2**self.phase1
            nQ = 2**self.phase2
            nI = 2**self.phase1
            nI += 2**self.phase2

            awg = 0
            awg_lag = 2
        elif self.phase_control =='awg':
            I = 0
            Q = 0
            nQ = 0
            nI = 0

            awg = 2** self.awg
            awg_lag = self.awg_lag

        mw = 2**self.mw
        aom = 2**self.aom
        daq = 2**self.daq

        if pi2 == 0:
            mw = 0

        n_reps = n_reps//2

        pi2 += pi2_offset

        self.start_programming()
        self.inst(0, Inst.LOOP, n_reps, 100)
        #self.inst(awg, Inst.CONTINUE, 0, awg_lag)
        # Pulse
        self.inst(daq, Inst.CONTINUE, 0, readout_buffer)
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        self.inst(I, Inst.CONTINUE, 0, readout_buffer)
        self.inst(aom, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.CONTINUE, 0, off_time)
        # Reference
        self.inst(aom, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.CONTINUE, 0, pi2)
        self.inst(0, Inst.CONTINUE, 0, readout_buffer)
        self.inst(aom, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.END_LOOP, 0, off_time)
        # End
        self.inst(0, Inst.STOP, 0, 100)
        self.stop_programming()

        rep_time = (readout_buffer+ init_time + pi2 + readout_buffer + init_time + off_time)

        return rep_time / 1e9



    def setup_t1(self, delay, pi2, pi2_offset, n_reps,
                          off_time=500,
                          init_time=15000):
        '''     
        Performs  mw pi pulse, delay, pi/2 pulse and readout for 
        NV T1 measurement

        Required pb channels: phase1, phase2, aom, daq, mw

        inputs:
            delay - delay between pi and pi/2 for readout
                in ns
            pi2 - pi2 pulse time in ns
            pi2_offset - constant offset for pi2, pi etc pulse scaling
            n_reps - number of on/ref repeats
            off_time - time between on/off in ns
            init_time - aom initialization time in ns
        returns:
            (float) time in (s) for one 'cycle' of either
            signal or reference

        Sequence:
        
        aom+I - init_time
        mw+I - pi
        I - delay
        mw+I - pi/2
        0 - readout_buffer
        aom + daq - init_time
        0 - off time

        aom+I - init_time
        mw+I - pi
        -I - delay
        mw+-I - pi/2
        0 - readout_buffer
        aom + daq - init_time
        0 - off time

        '''

        if self.phase_control == 'switches':
            I = 0
            Q = 2**self.phase1
            nQ = 2**self.phase2
            nI = 2**self.phase1
            nI += 2**self.phase2

            awg = 0
            awg_lag = 2
        elif self.phase_control =='awg':
            I = 0
            Q = 0
            nQ = 0
            nI = 0

            awg = 2** self.awg
            awg_lag = self.awg_lag

        mw = 2**self.mw
        aom = 2**self.aom
        daq = 2**self.daq

        if pi2 == 0:
            mw = 0

        n_reps = n_reps//2

        pi2 += pi2_offset
        pi = 2*pi2 - pi2_offset

        self.stop()
        self.start_programming()
        self.inst(0, Inst.LOOP, n_reps, 100)
        self.inst(awg, Inst.CONTINUE, 0, awg_lag)
        # invert spins
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(mw + I, Inst.CONTINUE, 0, pi)
        self.inst(I, Inst.CONTINUE, 0, delay)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.CONTINUE, 0, off_time)
        # reference scan
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.CONTINUE, 0, pi)
        self.inst(0, Inst.CONTINUE, 0, delay)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.END_LOOP, 0, off_time)
        # end
        self.inst(0, Inst.STOP, 0, 100)
        self.stop_programming()
        self.reset()

        rep_time = (2*init_time + pi  + delay + off_time)

        return rep_time / 1e9

    def setup_hahn_echo(
        self, delay, pi2, pi2_offset, n_reps,
        off_time=500,
        init_time=15000,
        readout_buffer=10):
        '''     
        Performs hahn echo sequence
        pi/2(x) - delay - pi(x) - delay - pi2(x)
        pi/2(x) - delay - pi(x) - delay - pi2(-x)

        Required pb channels: phase1, phase2, aom, daq, mw

        inputs:
            delay - delay between pi/2 - pi and pi-pi/2 for readout
                in ns
            pi2 - pi2 pulse time in ns
            pi - pi pulse time in ns
            n_reps - number of on/ref repeats
            off_time - time between on/off in ns
            init_time - aom initialization time in ns
            readout_buffer - time between last mw pulse and readout
        returns:
            (float) time in (s) for one 'cycle' which includes
            signal and reference
        '''

        if self.phase_control == 'switches':
            I = 0
            Q = 2**self.phase1
            nQ = 2**self.phase2
            nI = 2**self.phase1
            nI += 2**self.phase2

            awg = 0
            awg_lag = 2
        elif self.phase_control =='awg':
            I = 0
            Q = 0
            nQ = 0
            nI = 0

            awg = 2** self.awg
            awg_lag = self.awg_lag
        mw = 2**self.mw
        aom = 2**self.aom
        daq = 2**self.daq

        if pi2 == 0:
            mw = 0

        n_reps = n_reps//2

        pi = pi2_offset + 2 * pi2
        pi32 = 3*pi2 + pi2_offset
        pi2 += pi2_offset

        self.stop()
        self.start_programming()
        self.inst(0, Inst.LOOP, n_reps, 100)
        self.inst(awg, Inst.CONTINUE, 0, awg_lag)
        # end pi/2 pulse
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        self.inst(Q, Inst.CONTINUE, 0, delay)
        self.inst(mw + Q, Inst.CONTINUE, 0, pi)
        if self.phase_control=='switches':
                self.inst(I, Inst.CONTINUE, 0, delay)
                self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        elif self.phase_control=='awg':
                self.inst(I, Inst.CONTINUE, 0, delay)
                self.inst(mw + I, Inst.CONTINUE, 0, pi2)
                self.inst(0, Inst.CONTINUE, 0, pi - pi2_offset)
        self.inst(0, Inst.CONTINUE, 0, readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.CONTINUE, 0, off_time)
        # end 3pi/2 pulse
        self.inst(aom, Inst.CONTINUE, 0, init_time)
        self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        self.inst(Q, Inst.CONTINUE, 0, delay)
        self.inst(mw + Q, Inst.CONTINUE, 0, pi)
        if self.phase_control=='switches':
            self.inst(nI, Inst.CONTINUE, 0, delay)
            self.inst(mw + nI, Inst.CONTINUE, 0, pi2)
        elif self.phase_control=='awg':
            self.inst(I, Inst.CONTINUE, 0, delay)
            self.inst(mw + I, Inst.CONTINUE, 0, pi32)
        self.inst(0, Inst.CONTINUE, 0, readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.END_LOOP, 0, off_time)
        # end
        self.inst(0, Inst.STOP, 0, 100)
        self.stop_programming()
        self.reset()

        rep_time = (
            2 * init_time + 
            2 * pi2 + 
            pi + 
            2 * delay + 
            off_time + 
            readout_buffer)

        if self.phase_control=='awg':
            rep_time += pi - pi2_offset

        return rep_time / 1e9

    def setup_hahn_echo_correlation(
        self, delay, pi2, pi2_offset, n_reps, corr_time,
        off_time=500,
        init_time=15000,
        readout_buffer=10):
        '''     
        Performs hahn echo sequence
        pi/2(x) - delay - pi(x) - delay - pi2(x)
        pi/2(x) - delay - pi(x) - delay - pi2(-x)

        Required pb channels: phase1, phase2, aom, daq, mw

        inputs:
            delay - delay between pi/2 - pi and pi-pi/2 for readout
                in ns
            pi2 - pi2 pulse time in ns
            pi - pi pulse time in ns
            n_reps - number of on/ref repeats
            off_time - time between on/off in ns
            init_time - aom initialization time in ns
            readout_buffer - time between last mw pulse and readout
        returns:
            (float) time in (s) for one 'cycle' which includes
            signal and reference
        '''

        if self.phase_control == 'switches':
            I = 0
            Q = 2**self.phase1
            nQ = 2**self.phase2
            nI = 2**self.phase1
            nI += 2**self.phase2

            awg = 0
            awg_lag = 2
        elif self.phase_control =='awg':
            I = 0
            Q = 0
            nQ = 0
            nI = 0

            awg = 2** self.awg
            awg_lag = self.awg_lag
        mw = 2**self.mw
        aom = 2**self.aom
        daq = 2**self.daq

        if pi2 == 0:
            mw = 0

        n_reps = n_reps//2

        pi = pi2_offset + 2 * pi2
        pi32 = 3*pi2 + pi2_offset
        pi2 += pi2_offset

        self.stop()
        self.start_programming()
        self.inst(0, Inst.LOOP, n_reps, 100)
        self.inst(awg, Inst.CONTINUE, 0, awg_lag)

        # end pi/2 pulse
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        self.inst(I, Inst.CONTINUE, 0, delay)
        self.inst(mw + I, Inst.CONTINUE, 0, pi)
        self.inst(Q, Inst.CONTINUE, 0, delay)
        self.inst(mw + Q, Inst.CONTINUE, 0, pi2)

        self.inst(I, Inst.CONTINUE, 0, corr_time)

        self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        self.inst(I, Inst.CONTINUE, 0, delay)
        self.inst(mw + I, Inst.CONTINUE, 0, pi)
        self.inst(Q, Inst.CONTINUE, 0, delay)
        self.inst(mw + Q, Inst.CONTINUE, 0, pi2)

        self.inst(0, Inst.CONTINUE, 0, readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.CONTINUE, 0, off_time)

        # end 3pi/2 pulse

        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        self.inst(I, Inst.CONTINUE, 0, delay)
        self.inst(mw + I, Inst.CONTINUE, 0, pi)
        self.inst(Q, Inst.CONTINUE, 0, delay)
        self.inst(mw + Q, Inst.CONTINUE, 0, pi2)

        self.inst(I, Inst.CONTINUE, 0, corr_time)

        self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        self.inst(I, Inst.CONTINUE, 0, delay)
        self.inst(mw + I, Inst.CONTINUE, 0, pi)
        self.inst(nQ, Inst.CONTINUE, 0, delay)
        self.inst(mw + nQ, Inst.CONTINUE, 0, pi2)

        self.inst(0, Inst.CONTINUE, 0, readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.END_LOOP, 0, off_time)
        # end
        self.inst(0, Inst.STOP, 0, 100)
        self.stop_programming()
        self.reset()

        rep_time = (
            2 * init_time + 
            4 * pi2 + 
            2* pi + 
            4 * delay + 
            off_time + 
            corr_time + 
            readout_buffer)

        return rep_time / 1e9

    def setup_ramsey(
        self, pi2, pi2_offset, delay, n_reps,
        off_time=500,
        init_time=15000,
        readout_buffer=2000):

        if self.phase_control == 'switches':
            I = 0
            Q = 2**self.phase1
            nQ = 2**self.phase2
            nI = 2**self.phase1
            nI += 2**self.phase2

            awg = 0
            awg_lag = 2
        elif self.phase_control =='awg':
            I = 0
            Q = 0
            nQ = 0
            nI = 0

            awg = 2** self.awg
            awg_lag = self.awg_lag
        mw = 2**self.mw
        aom = 2**self.aom
        daq = 2**self.daq

        if pi2 == 0:
            mw = 0

        n_reps = n_reps//2

        pi2 += pi2_offset
        pi = 2*pi2 - pi2_offset

        self.stop()
        self.start_programming()
        self.inst(0, Inst.LOOP, n_reps, 100)
        self.inst(awg, Inst.CONTINUE, 0, awg_lag)
        # First ramsey -z projection
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        self.inst(I, Inst.CONTINUE, 0, delay)   
        self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        self.inst(0, Inst.CONTINUE, 0, readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.CONTINUE, 0, off_time)
        # Second ramsey +z projection
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        self.inst(nI, Inst.CONTINUE, 0, delay)
        self.inst(mw + nI, Inst.CONTINUE, 0, pi2)
        self.inst(0, Inst.CONTINUE, 0, readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.END_LOOP, 0, off_time)
        # Exit
        self.inst(0, Inst.STOP, 0, 100)
        self.stop_programming()
        self.reset()

        rep_time = 2*init_time + 2*pi + delay + readout_buffer + off_time

        return rep_time/1e9


    def setup_cpmgxy8n(
        self, delay, pi2, pi2_offset, n_reps, nxy8,
        off_time=500,
        init_time=15000,
        readout_buffer=2000):
        ''' 
        Sets up CPMGXY8N pulse sequence
        pi/2(x) - CPMGXY8-N - pi2/(x)
        pi/2(x) - CPMGXY8-N - 3*pi2/(x)


        '''
        if self.phase_control == 'switches':
            I = 0
            Q = 2**self.phase1
            nQ = 2**self.phase2
            nI = 2**self.phase1
            nI += 2**self.phase2

            awg = 0
            awg_lag = 2
        elif self.phase_control =='awg':
            I = 0
            Q = 0
            nQ = 0
            nI = 0

            awg = 2** self.awg
            awg_lag = self.awg_lag

        if delay % 2 != 0:
            delays = self.make_quantum_interpolation_delays(
                self.sample_rate, delay, nxy8)
        else:
            delays = [delay for i in range(2 * 8 * nxy8)]
    
        phases = []
        for i in range(nxy8):
            phases += [I, Q, I, Q, Q, I, Q, I]

        mw = 2**self.mw
        aom = 2**self.aom
        daq = 2**self.daq

        if pi2 == 0:
            mw = 0

        n_reps = n_reps//2

        pi = 2*pi2+pi2_offset
        pi32 = 3*pi2 + pi2_offset
        pi2 = pi2 + pi2_offset

        self.stop()
        self.start_programming()
        self.inst(0, Inst.LOOP, n_reps, 100)
        ## First CPMGXY8-n -z projection
        # Tip
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(awg, Inst.CONTINUE, 0, awg_lag)
        self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        # CPMG sequence
        self.make_cpmg_pulses(pi, delays, phases, nI)
        # Project and readout
        self.inst(mw + nI, Inst.CONTINUE, 0, pi2) 
        self.inst(0, Inst.CONTINUE, 0, readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.CONTINUE, 0, off_time)

        ## Second CPMGXY8-N z projection
        # Tip
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(awg, Inst.CONTINUE, 0, awg_lag)
        self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        # CPMG
        self.make_cpmg_pulses(pi, delays, phases, I)
        # Project and readout
        self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        self.inst(0, Inst.CONTINUE, 0, readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.END_LOOP, 0, off_time)
        # Exit loop
        self.inst(0, Inst.STOP, 0, 100)
        self.stop_programming()
        self.reset()

        rep_time = (
            2 * init_time +
            4 * (pi2 + pi2_offset) +
            8 * nxy8 * 2*(pi2+ pi2_offset) +
            (2 * 8 * nxy8) * delay +
            readout_buffer +
            init_time +
            off_time
            )

        return rep_time/1e9

        # self.stop()
        # self.start_programming()
        # self.inst(0, Inst.LOOP, n_reps, 100)
        # self.inst(awg, Inst.CONTINUE, 0, awg_lag)
        # ## First CPMGXY8-n -z projection
        # # Tip
        # self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        # self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        # # CPMG sequence
        # self.make_cpmg_pulses(pi, delays, phases, I)
        # # Project and readout
        # self.inst(mw + I, Inst.CONTINUE, 0, pi2) 
        # self.inst(0, Inst.CONTINUE, 0, readout_buffer)
        # self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        # self.inst(0, Inst.CONTINUE, 0, off_time)

        # ## Second CPMGXY8-N z projection
        # # Tip
        # self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        # self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        # # CPMG
        # self.make_cpmg_pulses(pi, delays, phases, nI)
        # # Project and readout
        # self.inst(mw + nI, Inst.CONTINUE, 0, pi2)
        # self.inst(0, Inst.CONTINUE, 0, readout_buffer)
        # self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        # self.inst(0, Inst.END_LOOP, 0, off_time)
        # # Exit loop
        # self.inst(0, Inst.STOP, 0, 100)
        # self.stop_programming()
        # self.reset()

        # rep_time = (
        #     2 * init_time +
        #     4 * (pi2 + pi2_offset) +
        #     8 * nxy8 * 2*(pi2+ pi2_offset) +
        #     (2 * 8 * nxy8) * delay +
        #     readout_buffer +
        #     init_time +
        #     off_time
        #     )

        # return rep_time/1e9


    def setup_cpmgxy8n_corr(
        self, delay, pi2, pi2_offset, n_reps, nxy8, corr_time,
        readout_buffer=2000,
        off_time=500,
        init_time=15000):
        '''     
        Performs  cpmgxy8xN - corr_time cpmgxy8xN sequence
        and readout for NV Correlation spectroscopy

        Required pb channels: phase1, phase2, aom, daq, mw

        inputs:
            delay - delay between pi/2 - pi and pi-pi/2 for readout
                in ns
            corr_time - time between cpmgxy8N sequences
            pi2 - pi2 pulse time in ns
            pi - pi pulse time in ns
            nxy8 - number of xy8 sequences
            sample_rate - sample rate for the pulse sequence used
                to calculate quantum interplation sequence in Hz
            n_reps - number of on/ref repeats
            off_time - time between on/off in ns
            init_time - aom initialization time in ns
            readout_buffer - time between last mw pulse and readout
        returns:
            (float) time in (s) for one 'cycle' which includes
            signal and reference

        Sequence:
        
        aom+I - init_time
        mw+I - pi/2
        CPMGXY8N
        mw+Q - pi/2
        0 - correlation time
        mw+I - pi/2
        CPMGXY8N
        mw+Q - pi/2
        0 - readout_buffer
        aom+daq - init_time
        off_time

        aom+I - init_time
        mw+I - pi/2
        CPMGXY8N
        mw+Q - pi/2
        0 - correlation time
        mw+I - pi/2
        CPMGXY8N
        mw+-Q - pi/2
        0 - readout_buffer
        aom+daq - init_time
        off_time
        '''

        if self.phase_control == 'switches':
            I = 0
            Q = 2**self.phase1
            nQ = 2**self.phase2
            nI = 2**self.phase1
            nI += 2**self.phase2

            awg = 0
            awg_lag = 2
        elif self.phase_control =='awg':
            I = 0
            Q = 0
            nQ = 0
            nI = 0

            awg = 2** self.awg
            awg_lag = self.awg_lag

        if delay % 2 != 0:
            delays = self.make_quantum_interpolation_delays(
                self.sample_rate, delay, nxy8)
        else:
            delays = [delay for i in range(2*nxy8 + 1)]
        
        mw = 2**self.mw
        aom = 2**self.aom
        daq = 2**self.daq

        phases = []
        for i in range(nxy8):
            phases += [I, Q, I, Q, Q, I, Q, I]

        if pi2 == 0:
            mw = 0
        
        n_reps = n_reps//2

        pi2 += pi2_offset
        pi = 2*pi2 - pi2_offset
        pi2x3 = 3*pi2 - 2*pi2_offset

        self.stop()
        self.start_programming()
        self.inst(0, Inst.LOOP, n_reps, 100)
        self.inst(awg, Inst.CONTINUE, 0, awg_lag)
        # First, project to -z
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        self.make_cpmg_pulses(pi, delays, phases, Q)
        self.inst(mw + Q, Inst.CONTINUE, 0, pi2)

        # self.inst(Q, Inst.CONTINUE, 0, corr_time)
        self.inst(Q, Inst.CONTINUE, 0, corr_time)

        self.inst(mw + Q, Inst.CONTINUE, 0, pi2)
        self.make_cpmg_pulses(pi, delays, phases, I)
        self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        self.inst(0, Inst.CONTINUE, 0, readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.CONTINUE, 0, off_time)

        # Second reference run, project to +z
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        # testing
        # self.make_cpmg_pulses(pi,delays,phases,nQ)
        # self.inst(mw + nQ, Inst.CONTINUE, 0, pi2)

        # self.inst(nQ, Inst.CONTINUE, 0, corr_time+pi)

        # self.inst(mw + nQ, Inst.CONTINUE, 0, pi2)
        # self.make_cpmg_pulses(pi, delays, phases, I)
        # self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        # testing end
        self.make_cpmg_pulses(pi, delays, phases, Q)
        self.inst(mw + Q, Inst.CONTINUE, 0, pi2)

        self.inst(Q, Inst.CONTINUE, 0, corr_time)

        self.inst(mw + Q, Inst.CONTINUE, 0, pi2)
        self.make_cpmg_pulses(pi, delays, phases, nI)
        self.inst(mw + nI, Inst.CONTINUE, 0, pi2)
        self.inst(0, Inst.CONTINUE, 0, readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.END_LOOP, 0, off_time)
        # End an exit
        self.inst(0, Inst.STOP, 0, 100)
        self.stop_programming()
        self.reset()

 
        rep_time = (
            2 * init_time +
            6 * pi2 +
            2* 8 * nxy8 * pi +
            2* (8 * nxy8 + 1) * delay +
            readout_buffer +
            init_time +
            off_time +
            corr_time
            )

        return rep_time/1e9
        # n_reps = n_reps//2

        # pi2 += pi2_offset
        # pi = 2*pi2 - pi2_offset
        # pi2x3 = 3*pi2 - 2*pi2_offset

        # self.stop()
        # self.start_programming()
        # self.inst(0, Inst.LOOP, n_reps, 100)
        # self.inst(awg, Inst.CONTINUE, 0, awg_lag)
        # # First, project to -z
        # self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        # self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        # # self.make_cpmg_pulses(pi, delay, phases, nxy8, Q)
        # self.make_cpmg_pulses(pi, delays, phases, Q)
        # self.inst(mw + Q, Inst.CONTINUE, 0, pi2)

        # self.inst(I, Inst.CONTINUE, 0, corr_time)

        # self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        # # self.make_cpmg_pulses(pi, delay, phases, nxy8, Q
        # self.make_cpmg_pulses(pi, delays, phases, I)
        # self.inst(mw + Q, Inst.CONTINUE, 0, pi2)
        # self.inst(0, Inst.CONTINUE, 0, pi2*2)
        # self.inst(0, Inst.CONTINUE, 0, readout_buffer)
        # self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        # self.inst(0, Inst.CONTINUE, 0, off_time)

        # # Second reference run, project to +z
        # self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        # self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        # self.inst(I, Inst.CONTINUE, 0, delay)
        # # self.make_cpmg_pulses(pi, delay, phases, nxy8, Q)
        # self.make_cpmg_pulses(pi, delays, phases, Q)
        # self.inst(mw + Q, Inst.CONTINUE, 0, pi2)

        # self.inst(I, Inst.CONTINUE, 0, corr_time)

        # self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        # self.inst(I, Inst.CONTINUE, 0, delay)
        # # self.make_cpmg_pulses(pi, delay, phases, nxy8, Q)
        # self.make_cpmg_pulses(pi, delays, phases, nI)
        # self.inst(mw + Q, Inst.CONTINUE, 0, pi2)
        # self.inst(mw + Q, Inst.CONTINUE, 0, pi2*2)
        # self.inst(0, Inst.CONTINUE, 0, readout_buffer)
        # self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        # self.inst(0, Inst.END_LOOP, 0, off_time)
        # # End an exit
        # self.inst(0, Inst.STOP, 0, 100)
        # self.stop_programming()
        # self.reset()

        # rep_time = (
        #     2 * init_time +
        #     6 * pi2 +
        #     2* 8 * nxy8 * pi +
        #     2* (8 * nxy8 + 1) * delay +
        #     readout_buffer +
        #     init_time +
        #     off_time +
        #     corr_time
        #     )

        # return rep_time/1e9

    def setup_cpmgxy16n(
        self, delay, pi2, pi2_offset, n_reps, nxy16,
        off_time=500,
        init_time=15000,
        readout_buffer=10):

        if self.phase_control == 'switches':
            I = 0
            Q = 2**self.phase1
            nQ = 2**self.phase2
            nI = 2**self.phase1
            nI += 2**self.phase2

            awg = 0
            awg_lag = 2
        elif self.phase_control =='awg':
            I = 0
            Q = 0
            nQ = 0
            nI = 0

            awg = 2** self.awg
            awg_lag = self.awg_lag

        if delay % 2 != 0:
            delays = self.make_quantum_interpolation_delays(
                self.sample_rate, delay, nxy16)
        else:
            delays = [delay for i in range(2 * 16 * nxy16 + 1)]
    
        mw = 2**self.mw
        aom = 2**self.aom
        daq = 2**self.daq

        if pi2 == 0:
            mw = 0

        n_reps = n_reps//2

        pi2 += pi2_offset
        pi = 2*pi2 - pi2_offset
        pi2x3 = 3*pi2 - 2*pi2_offset

        self.stop()
        self.start_programming()
        self.inst(0, Inst.LOOP, n_reps, 100)
        self.inst(awg, Inst.CONTINUE, 0, awg_lag)
        # First CPMGXY8-n -z projection
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(mw + I, Inst.CONTINUE, 0, pi2) 
        self.make_cpmgxy16n_pulses(pi, delay, phases, I)
        self.inst(mw + I, Inst.CONTINUE, 0, pi2) 
        self.inst(0, Inst.CONTINUE, 0, pi2*2) 
        self.inst(0, Inst.CONTINUE, 0, readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.CONTINUE, 0, off_time)

        # Second CPMGXY8-N z projection
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(mw + I, Inst.CONTINUE, 0, pi2) # pi2-x
        self.make_cpmgxy16n_pulses(pi, delays, phases, end_phase)
        self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        self.inst(mw + I, Inst.CONTINUE, 0, pi2 * 2)
        self.inst(0, Inst.CONTINUE, 0, readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.END_LOOP, 0, off_time)
        # Exit loop
        self.inst(0, Inst.STOP, 0, 100)
        self.stop_programming()
        self.reset()

        rep_time = (
            2 * init_time +
            4 * pi2 +
            16 * nxy16 * pi +
            (16 * nxy16 + 1) * delay +
            readout_buffer +
            init_time +
            off_time
            )

        return rep_time/1e9


    def setup_cpmgxy16n_corr(
        self, delay, pi2, pi2_offset, n_reps, nxy16, corr_time,
        readout_buffer=2000,
        off_time=500,
        init_time=15000):
        '''     
        Performs  cpmgxy16xN - corr_time cpmgxy16xN sequence
        and readout for NV Correlation spectroscopy

        Required pb channels: phase1, phase2, aom, daq, mw

        inputs:
            delay - delay between pi/2 - pi and pi-pi/2 for readout
                in ns
            corr_time - time between cpmgxy8N sequences
            pi2 - pi2 pulse time in ns
            pi - pi pulse time in ns
            nxy8 - number of xy8 sequences
            sample_rate - sample rate for the pulse sequence used
                to calculate quantum interplation sequence in Hz
            n_reps - number of on/ref repeats
            off_time - time between on/off in ns
            init_time - aom initialization time in ns
            readout_buffer - time between last mw pulse and readout
        returns:
            (float) time in (s) for one 'cycle' which includes
            signal and reference

        Sequence:
        
        aom+I - init_time
        mw+I - pi/2
        CPMGXY16N
        mw+Q - pi/2
        0 - correlation time
        mw+I - pi/2
        CPMGXY16N
        mw+Q - pi/2
        0 - readout_buffer
        aom+daq - init_time
        off_time

        aom+I - init_time
        mw+I - pi/2
        CPMGXY16N
        mw+Q - pi/2
        0 - correlation time
        mw+I - pi/2
        CPMGXY16N
        mw+-Q - pi/2
        0 - readout_buffer
        aom+daq - init_time
        off_time
        '''

        if self.phase_control == 'switches':
            I = 0
            Q = 2**self.phase1
            nQ = 2**self.phase2
            nI = 2**self.phase1
            nI += 2**self.phase2

            awg = 0
            awg_lag = 2
        elif self.phase_control =='awg':
            I = 0
            Q = 0
            nQ = 0
            nI = 0

            awg = 2** self.awg
            awg_lag = self.awg_lag

        if delay % 2 != 0:
            delays = self.make_quantum_interpolation_delays(
                self.sample_rate, delay, nxy16)
        else:
            delays = [delay for i in range(2 * 16 * nxy16 + 1)]

        phases = []    
        for i in range(nxy8):
            phases += [I, Q, I, Q, Q, I, Q, I,
                       nI, nQ, nI, nQ, nQ, nI, nQ, nI]

        mw = 2**self.mw
        aom = 2**self.aom
        daq = 2**self.daq

        if pi2 == 0:
            mw = 0

        pi2 += pi2_offset
        pi = 2*pi2 - pi2_offset
        pi2x3 = 3*pi2 - 2*pi2_offset

        self.stop()
        self.start_programming()
        self.inst(0, Inst.LOOP, n_cycles, 100)
        self.inst(awg, Inst.CONTINUE, 0, awg_lag)
        # First, project to -z
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        self.make_cpmgxy_pulses(pi, delay, phases, Q)
        self.inst(mw + Q, Inst.CONTINUE, 0, pi2)

        self.inst(I, Inst.CONTINUE, 0, corr_time)

        self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        self.make_cpmgxy16n_pulses(pi, delay, phases, Q)
        self.inst(mw + Q, Inst.CONTINUE, 0, pi2)
        self.inst(0, Inst.CONTINUE, 0, 2*pi2 - 2*pi2offset)
        self.inst(0, Inst.CONTINUE, 0, readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.CONTINUE, 0, off_time)

        # Second reference run, project to +z
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        self.inst(I, Inst.CONTINUE, 0, delay)
        self.make_cpmgxy_pulses(pi, delays, phases, Q)
        self.inst(mw + Q, Inst.CONTINUE, 0, pi2)

        self.inst(I, Inst.CONTINUE, 0, corr_time)

        self.inst(mw + I, Inst.CONTINUE, 0, pi2)
        self.inst(I, Inst.CONTINUE, 0, delay)
        self.make_cpmgxy16n_pulses(pi, delays, phases, Q)
        self.inst(mw + Q, Inst.CONTINUE, 0, p2x3)
        self.inst(0, Inst.CONTINUE, 0, readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.END_LOOP, 0, off_time)
        # End an exit
        self.inst(0, Inst.STOP, 0, 100)
        self.stop_programming()
        self.reset()

        rep_time = (
            2 * init_time +
            4 * pi2 +
            2* 16 * nxy8 * pi +
            2* (16 * nxy8 + 1) * delay +
            readout_buffer +
            init_time +
            off_time +
            corr_time
            )

        return rep_time/1e9


    def make_quantum_interpolation_delays(self,
        sample_rate, delay, nxy8):

        dt = 1/(sample_rate*1e-9)
        tau = delay//dt*dt
        U_0 = [tau,tau, tau,tau]
        U_1 = [tau+dt, tau+dt, tau+dt, tau+dt]
        sample =  np.round(delay%dt/dt*(4*nxy8))/(4*nxy8)
        delays = np.array([])

        m =0
        for j in range(4*nxy8):
            m = m + sample
            if np.abs(m) <= 1/2:
                delays = np.append(delays,U_0)
            else:
                delays = np.append(delays,U_1)
                m -=1

        return delays//dt*dt

    def make_cpmg_pulses(self, pi, delays, phases, end_phase):
        '''
        Programs pulseblaster to execute cpmg-N pulses

        Inputs:
            pi (int) - pi pulse time
            delays (array (int)) - array of 2*n (8 or 16)+1 delays
            phases array(int) - array of phase cycles
            end_phase (int) last phase for readout setup

        returns:
            None

        '''

        tempPhases  = phases.copy()
        tempPhases += [end_phase]
        mw = 2 ** self.mw
        for i in range(len(delays)//2):
            self.inst(tempPhases[i], Inst.CONTINUE, 0, delays[2*i])
            self.inst(mw + tempPhases[i], Inst.CONTINUE, 0, pi)
            self.inst(tempPhases[i+1], Inst.CONTINUE, 0, delays[2*i + 1])

    def setup_t1_DQ1(self, delay, pi2, pi2_offset, n_reps,
                          readout_buffer=10,
                          off_time=500,
                          init_time=15000):
        '''     
        Performs  reference cycle (now MW pulse), followed by delay & pi pulse and readout for 
        NV T1 measurement

        Required pb channels: phase1, phase2, aom, daq, mw

        inputs:
            delay - delay between pi and pi/2 for readout
                in ns
            pi2 - pi2 pulse time in ns
            pi2_offset - constant offset for pi2, pi etc pulse scaling
            n_reps - number of on/ref repeats
            off_time - time between on/off in ns
            init_time - aom initialization time in ns
        returns:
            (float) time in (s) for one 'cycle' of either
            signal or reference

        Sequence:
        
        aom+I - init_time
        0 - pi
        0 - delay
        0 - pi
        0 - readout_buffer
        aom + daq - init_time
        0 - off time

        aom+I - init_time
        0 - pi
        0 - delay
        mw+-I - pi
        0 - readout_buffer
        aom + daq - init_time
        0 - off time

        '''

        if self.phase_control == 'switches':
            I = 0
            Q = 2**self.phase1
            nQ = 2**self.phase2
            nI = 2**self.phase1
            nI += 2**self.phase2

            awg = 0
            awg_lag = 2
        elif self.phase_control =='awg':
            I = 0
            Q = 0
            nQ = 0
            nI = 0

            awg = 2** self.awg
            awg_lag = self.awg_lag

        mw = 2**self.mw
        aom = 2**self.aom
        daq = 2**self.daq

        if pi2 == 0:
            mw = 0

        n_reps = n_reps//2

        pi2 += pi2_offset
        pi = 2*pi2 - pi2_offset

        self.stop()
        self.start_programming()
        self.inst(0, Inst.LOOP, n_reps, 100)
        self.inst(awg, Inst.CONTINUE, 0, awg_lag)
        # invert spins
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.CONTINUE, 0, pi)
        self.inst(I, Inst.CONTINUE, 0, delay)
        self.inst(0, Inst.CONTINUE, 0, pi)
        self.inst(0, Inst.CONTINUE, 0 , readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.CONTINUE, 0, off_time)
        # reference scan
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.CONTINUE, 0, pi)
        self.inst(0, Inst.CONTINUE, 0, delay)
        self.inst(mw + I, Inst.CONTINUE, 0, pi)
        self.inst(0, Inst.CONTINUE, 0 , readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.END_LOOP, 0, off_time)
        # end
        self.inst(0, Inst.STOP, 0, 100)
        self.stop_programming()
        self.reset()

        rep_time = (2*init_time + 2*pi  + delay + readout_buffer+ off_time)

        return rep_time / 1e9
        
    def setup_t1_DQ2(self, delay, pi2, pi2_offset,pi22,pi22_offset, n_reps,
                          readout_buffer=10,
                          off_time=500,
                          init_time=15000):
        '''     
        Measurement to estimate transfer rate b/w excited states (-1/+1)
        First sequence(reference): initialize-(-1)pi-delay-(-1)pi-buffer-readout
        Second sequence: initialize-(-1)pi-delay-(+1)pi-buffer-readout

        Required pb channels: phase1, phase2, aom, daq, mw, mw2

        inputs:
            delay - delay between pi and pi/2 for readout
                in ns
            pi2 - pi2 pulse time of 0/-1 transition in ns
            pi2_offset - constant offset for pi2, pi etc pulse scaling
            pi22 - pi2 pulse of 0/+1 transition in ns
            n_reps - number of on/ref repeats
            off_time - time between on/off in ns
            init_time - aom initialization time in ns
        returns:
            (float) time in (s) for one 'cycle' of either
            signal or reference

        Sequence:
        
        aom+I - init_time
        mw+I - pi
        I - delay
        mw+I - pi
        0 - readout_buffer
        aom + daq - init_time
        0 - off time

        aom+I - init_time
        mw+I - pi
        -I - delay
        mw2+I - pi
        0 - readout_buffer
        aom + daq - init_time
        0 - off time

        '''

        if self.phase_control == 'switches':
            I = 0
            Q = 2**self.phase1
            nQ = 2**self.phase2
            nI = 2**self.phase1
            nI += 2**self.phase2


            awg = 0
            awg_lag = 2
        elif self.phase_control =='awg':
            I = 0
            Q = 0
            nQ = 0
            nI = 0

            awg = 2** self.awg
            awg_lag = self.awg_lag

        mw = 2**self.mw
        aom = 2**self.aom
        daq = 2**self.daq
        mw2 = 2**self.mw2

        if pi2 == 0:
            mw = 0

        n_reps = n_reps//2

        pi2 += pi2_offset
        pi = 2*pi2 - pi2_offset


        pi22 += pi22_offset
        pi_2 = 2*pi22 - pi22_offset

        self.stop()
        self.start_programming()
        self.inst(0, Inst.LOOP, n_reps, 100)
        self.inst(awg, Inst.CONTINUE, 0, awg_lag)
        # invert spins
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(mw+I, Inst.CONTINUE, 0, pi)
        self.inst(I, Inst.CONTINUE, 0, delay)
        self.inst(mw+I, Inst.CONTINUE, 0, pi)
        self.inst(0, Inst.CONTINUE, 0 , readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.CONTINUE, 0, off_time)
        # reference scan
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(mw+I, Inst.CONTINUE, 0, pi)
        self.inst(0, Inst.CONTINUE, 0, delay)
        self.inst(mw2 + I, Inst.CONTINUE, 0, pi_2)
        self.inst(0, Inst.CONTINUE, 0 , readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.END_LOOP, 0, off_time)
        # end
        self.inst(0, Inst.STOP, 0, 100)
        self.stop_programming()
        self.reset()

        rep_time = (2*init_time + 2*pi  + delay + off_time)

        return rep_time / 1e9


    def setup_t1_DQ_2b(self, delay, pi2, pi2_offset, n_reps,
                          readout_buffer=10,
                          off_time=500,
                          init_time=15000):
        '''     
        Alternative method to measure DQ without directly addressing ms=+1 transition (single MW source)
        First sequence is reference: initialize-pi pulse-delay-pi pulse-buffer-readout
        second sequence is measurement: initialize-pi delay-delay-pi pulse-buffer-readout

        Required pb channels: phase1, phase2, aom, daq, mw

        inputs:
            delay - delay between pi and pi/2 for readout
                in ns
            pi2 - pi2 pulse time in ns
            pi2_offset - constant offset for pi2, pi etc pulse scaling
            n_reps - number of on/ref repeats
            off_time - time between on/off in ns
            init_time - aom initialization time in ns
        returns:
            (float) time in (s) for one 'cycle' of either
            signal or reference

        Sequence:
        
        aom+I - init_time
        mw+I - pi
        I - delay
        mw+I - pi
        0 - readout_buffer
        aom + daq - init_time
        0 - off time

        aom+I - init_time
        0 - pi
        -I - delay
        mw+-I - pi
        0 - readout_buffer
        aom + daq - init_time
        0 - off time

        '''

        if self.phase_control == 'switches':
            I = 0
            Q = 2**self.phase1
            nQ = 2**self.phase2
            nI = 2**self.phase1
            nI += 2**self.phase2

            awg = 0
            awg_lag = 2
        elif self.phase_control =='awg':
            I = 0
            Q = 0
            nQ = 0
            nI = 0

            awg = 2** self.awg
            awg_lag = self.awg_lag

        mw = 2**self.mw
        aom = 2**self.aom
        daq = 2**self.daq

        if pi2 == 0:
            mw = 0

        n_reps = n_reps//2

        pi2 += pi2_offset
        pi = 2*pi2 - pi2_offset

        self.stop()
        self.start_programming()
        self.inst(0, Inst.LOOP, n_reps, 100)
        self.inst(awg, Inst.CONTINUE, 0, awg_lag)
        # invert spins
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(mw+I, Inst.CONTINUE, 0, pi)
        self.inst(I, Inst.CONTINUE, 0, delay)
        self.inst(mw+I, Inst.CONTINUE, 0, pi)
        self.inst(0, Inst.CONTINUE, 0 , readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.CONTINUE, 0, off_time)
        # reference scan
        self.inst(aom + I, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.CONTINUE, 0, pi)
        self.inst(0, Inst.CONTINUE, 0, delay)
        self.inst(mw + I, Inst.CONTINUE, 0, pi)
        self.inst(0, Inst.CONTINUE, 0 , readout_buffer)
        self.inst(aom + daq, Inst.CONTINUE, 0, init_time)
        self.inst(0, Inst.END_LOOP, 0, off_time)
        # end
        self.inst(0, Inst.STOP, 0, 100)
        self.stop_programming()
        self.reset()

        rep_time = (2*init_time + 2*pi  + delay + readout_buffer+ off_time)

        return rep_time / 1e9