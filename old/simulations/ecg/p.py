import math

def p(M_P,t_P,W_P,t):
	return M_P * math.exp(-1 * ((t - t_P)/(math.sqrt(2) * W_P)) ** 2)
