from .p_wave import p_wave
from .q_wave import q_wave
from .r_wave import r_wave
from .s_wave import s_wave
from .t_wave import t_wave
import numpy as np
import math

def returnDefault():
	P = [0.185, 0.0178, 0.2369]

	Q = [
			-0.1103, 0.03064, 0.3218,
			-0.1075, 0.005705, 0.37123,
		]

	R = [0.050, 0.02987, 0.46571]
	S = [0.509, 0.00909, 0.4769]
	T = [0.3255, 0.02978, 0.7543]

	return [P, Q, R, S, T]

def generateECG(sampling_frequency, noise_magnitude, end_time, period,
				P, Q, R, S, T, callback=None):

	begin_time = 0
	period = period
	end_time = end_time

	total_beats = int(end_time / period)

	if total_beats == 0:
		total_beats = 1

	begin = 0

	samples = sampling_frequency * total_beats

	x = np.linspace(begin_time, end_time, samples)

	noise = np.random.normal(0, noise_magnitude, x.shape)

	y = np.zeros(samples)

	for i in range(total_beats):
		y += p_wave(x, period * i, P)
		y += q_wave(x, period * i, Q)
		y += r_wave(x, period * i, R)
		y += s_wave(x, period * i, S)
		y += t_wave(x, period * i, T)

		if callback is not None:
			callback((i * 1.0) / total_beats) # percentage of completion

	output = y + noise

	return output