import math

def s(M_S,t_S,W_S,t):
	return -1 * M_S * math.exp(-1 * ((t - t_S)/(math.sqrt(2) * W_S)) ** 2)