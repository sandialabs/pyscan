# -*- coding: utf-8 -*-
"""
Plot Pulse Sequences
====================
"""

import matplotlib.pyplot as plt
import numpy as np
from pyscan.general.makepulsingarbs import *


def plot_ramsey(pi2, delay, phase=0, awg_lag=30, phase_lag=4, offset=True):
	'''
	Plot the pulse sequence for Ramsey pulses
	current incomplete

	Parameters
	----------
	pi2 :
		pi2 pulse time in ns
	delay : 
		Delay betwee pi2 pulses in ns
	phase :
		Phase of final pulse
	awg_lag :
		Lag time for the awg in ns
	phase_lag :
		Lag for application of phase
	offset :
		Offset x and y channels of pulse sequence
	'''

	fig, ax = plt.subplots(1, 1)

	x, y, mw = make_ramsey_phase_arbs(pi2, delay, phase, awg_lag, phase_lag)

	time = np.array(range(len(mw)))*2

	mwx = mw*x
	mwy = mw*y

	if offset:
		mwy+=2.5

	ax.plot(time, mwx)
	ax.plot(time, mwy)

	ax.set_xlabel('time (ns)')
	# plt.ylabel('amplitudes

	ax.set_yticks([-1, 0, 1, 1.5, 2.5, 3.5], ['-1', 'mw x', '1', '-1', 'mw y', '1'], minor=False)
