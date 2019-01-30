import argparse

def return_default():
	parser = argparse.ArgumentParser(description='Creating ECG Signal')

	parser.add_argument('-fs', '--sampling_freq', type=int, default=256, help='Sampling frequency of signal')

	parser.add_argument('-n', '--noise', type=float, default=0.01, help='Magnitude value of noise signal')

	parser.add_argument('-e', '--end_time', type=float, default=5, help='Stop time of the ECG Signal')
	parser.add_argument('-p', '--period', type=float, default=0.9, help='Period of the ECG Signal')

	parser.add_argument('-m_p', type=float, default=0.185, help='Magnitude of the P signal')
	parser.add_argument('-w_p', type=float, default=0.0178, help='Width of the P signal')
	parser.add_argument('-t_p', type=float, default=0.2369, help='Duration of the P signal')

	parser.add_argument('-m_q1', type=float, default=-0.1103, help='Magnitude of the Q1 signal')
	parser.add_argument('-w_q1', type=float, default=0.03064, help='Width of the Q1 signal')
	parser.add_argument('-t_q1', type=float, default=0.3218, help='Duration of the Q1 signal')

	parser.add_argument('-m_q2', type=float, default=-0.1075, help='Magnitude of the Q2 signal')
	parser.add_argument('-w_q2', type=float, default=0.005705, help='Width of the Q2 signal')
	parser.add_argument('-t_q2', type=float, default=0.37123, help='Duration of the Q2 signal')

	parser.add_argument('-m_r', type=float, default=0.050, help='Magnitude of the R signal')
	parser.add_argument('-w_r', type=float, default=0.02987, help='Width of the R signal')
	parser.add_argument('-t_r', type=float, default=0.46571, help='Duration of the R signal')

	parser.add_argument('-m_s', type=float, default=0.509, help='Magnitude of the S signal')
	parser.add_argument('-w_s', type=float, default=0.00909, help='Width of the S signal')
	parser.add_argument('-t_s', type=float, default=0.4769, help='Duration of the S signal')

	parser.add_argument('-m_t', type=float, default=0.3255, help='Magnitude of the T signal')
	parser.add_argument('-w_t', type=float, default=0.02978, help='Width of the T signal')
	parser.add_argument('-t_t', type=float, default=0.7543, help='Duration of the T signal')

	args = parser.parse_args()

	P = [args.m_p, args.w_p, args.t_p]

	Q = [
		 [args.m_q1, args.m_q2], 
		 [args.w_q1,  args.w_q2], 
		 [args.t_q1, args.t_q2]
		]

	R = [args.m_r, args.w_r, args.t_r]
	S = [args.m_s, args.w_s, args.t_s]
	T = [args.m_t, args.w_t, args.t_t]

	return args

# plt.plot(generateECG(args.sampling_freq, args.noise, args.end_time,
# 					 args.period, P, Q, R, S, T))
# plt.show()