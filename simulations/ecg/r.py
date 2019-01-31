import math

def r(M_R,t_R,W_R,t):
	possible_output = (-1 * M_R  * (t - t_R) * math.exp(-1 * ((t - t_R)/(math.sqrt(2) * W_R)) ** 2)) / (W_R ** 2)

	if possible_output < 0:
		return 0
	else:
		return possible_output