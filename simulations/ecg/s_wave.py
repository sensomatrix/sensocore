from .s import s
import numpy as np
import matplotlib.pyplot as plt

def s_wave(x, shift, S):
	y = x.copy()

	for i in range(len(x)):
		y[i] = s(S[0], S[2], S[1], x[i] - shift)

	return y