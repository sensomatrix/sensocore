from .p import p
from .q import q
from .r import r
from .s import s
from .t import t
import numpy as np
import math

def generateECG(sampling_frequency, noise_magnitude, end_time, period,
				P, Q, R, S, T, callback=None, is_for_graphing=True):

	Q = [
			[Q[0], Q[3]],
			[Q[1], Q[4]],
			[Q[2], Q[5]],
		]

	if is_for_graphing:
		end_time = period

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

	y += generateWave(x, period, total_beats, sampling_frequency, P, p)
	y += generateWave(x, period, total_beats, sampling_frequency, Q, q)
	y += generateWave(x, period, total_beats, sampling_frequency, R, r)
	y += generateWave(x, period, total_beats, sampling_frequency, S, s)
	y += generateWave(x, period, total_beats, sampling_frequency, T, t)

	if callback is not None:
		callback((i * 1.0) / total_beats) # percentage of completion

	output = y + noise

	return x, output

def generateWave(x, period, total_beats, sampling_frequency, wave_params, wave):
	y = x.copy()

	for beat in range(total_beats):
		shift = period * beat
		start_index = beat * sampling_frequency
		end_index = start_index + sampling_frequency

		for i in range(start_index, end_index):
			y[i] = wave(wave_params[0], wave_params[2], wave_params[1], x[i] - shift)

	return y