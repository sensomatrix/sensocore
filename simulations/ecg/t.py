import math

def t(M_T,t_T,W_T,t):
	return M_T * math.exp(-1 * ((t - t_T)/(math.sqrt(2) * W_T)) ** 2)