import math

def q(M_Q,t_Q,W_Q,t):
	return M_Q[0] * math.exp(-1 * ((t - t_Q[0])/(math.sqrt(2) * W_Q[0])) ** 2) + M_Q[1] * math.exp(-1 * ((t - t_Q[1])/(math.sqrt(2) * W_Q[1])) ** 2)