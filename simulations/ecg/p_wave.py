from .p import p
import numpy as np

def p_wave(x, shift, P):
	y = x.copy()

	for i in range(len(x)):
		y[i] = p(P[0], P[2], P[1], x[i] - shift)

	return y