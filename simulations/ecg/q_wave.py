from .q import q
import numpy as np
import matplotlib.pyplot as plt

def q_wave(x, shift, Q):
	y = x.copy()

	Q = [
			[Q[0], Q[3]],
			[Q[1], Q[4]],
			[Q[2], Q[5]],
		]

	for i in range(len(x)):
		y[i] = q(Q[0], Q[2], Q[1], x[i] - shift)

	return y