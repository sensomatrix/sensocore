from .q import q
import numpy as np
import matplotlib.pyplot as plt

def q_wave(x, shift, Q):
	y = x.copy()

	for i in range(len(x)):
		y[i] = q(Q[0], Q[2], Q[1], x[i] - shift)

	return y