from .r import r
import numpy as np
import matplotlib.pyplot as plt

def r_wave(x, shift, R):
	y = x.copy()

	for i in range(len(x)):
		y[i] = r(R[0], R[2], R[1], x[i] - shift)

	return y