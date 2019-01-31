from .t import t
import numpy as np
import matplotlib.pyplot as plt

def t_wave(x, shift, T):
	y = x.copy()

	for i in range(len(x)):
		y[i] = t(T[0], T[2], T[1], x[i] - shift)

	return y