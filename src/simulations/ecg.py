import numpy as np
import math


def p(M_P, t_P, W_P, t):
    return M_P * math.exp(-1 * ((t - t_P)/(math.sqrt(2) * W_P)) ** 2)


def q(M_Q, t_Q, W_Q, t):
    return M_Q[0] * math.exp(-1 * ((t - t_Q[0])/(math.sqrt(2) * W_Q[0])) ** 2) + M_Q[1] * math.exp(-1 * ((t - t_Q[1])/(math.sqrt(2) * W_Q[1])) ** 2)


def r(M_R, t_R, W_R, t):
    possible_output = (-1 * M_R * (t - t_R) * math.exp(-1 *
                                                       ((t - t_R)/(math.sqrt(2) * W_R)) ** 2)) / (W_R ** 2)

    if possible_output < 0:
        return 0
    else:
        return possible_output


def s(M_S, t_S, W_S, t):
    return -1 * M_S * math.exp(-1 * ((t - t_S)/(math.sqrt(2) * W_S)) ** 2)


def t(M_T, t_T, W_T, t):
    return M_T * math.exp(-1 * ((t - t_T)/(math.sqrt(2) * W_T)) ** 2)


def generate_ecg(sampling_frequency, noise_magnitude, end_time, period, delay,
                 P, Q, R, S, T, callback=None, is_for_graphing=True):

    Q = [
        [Q[0], Q[3]],
        [Q[1], Q[4]],
        [Q[2], Q[5]],
    ]

    begin_time = 0
    period = period
    end_time = end_time

    total_beats = int(end_time / period)

    if total_beats == 0:
        total_beats = 1

    if is_for_graphing:
        begin_time = delay
        end_time = begin_time + period
        total_beats = 1

    time_one_period = np.linspace(0, period, period * sampling_frequency)

    samples = sampling_frequency * total_beats

    diff = samples - len(time_one_period) * total_beats

    samples = samples - diff

    p_wave = np.tile(generateWave(time_one_period, P, p), total_beats)

    if callback is not None:
        callback(20)

    q_wave = np.tile(generateWave(time_one_period, Q, q), total_beats)

    if callback is not None:
        callback(40)

    r_wave = np.tile(generateWave(time_one_period, R, r), total_beats)

    if callback is not None:
        callback(60)

    s_wave = np.tile(generateWave(time_one_period, S, s), total_beats)

    if callback is not None:
        callback(80)

    t_wave = np.tile(generateWave(time_one_period, T, t), total_beats)

    x = np.linspace(begin_time, end_time, samples)

    y = p_wave + q_wave + r_wave + s_wave + t_wave

    y -= 0.2

    # Need to find out how much to shift the values by
    if not is_for_graphing:
        delay_shift = int(delay * sampling_frequency)

        y = np.roll(y, delay_shift)

        y[:delay_shift] = 0

    noise = np.random.normal(0, noise_magnitude, x.shape)

    output = y + noise

    if callback is not None:
        callback(100)

    x = np.reshape(x, (x.shape[0], 1))
    output = np.reshape(output, (output.shape[0], 1))

    ecg = np.hstack([x, output])

    return ecg


def generateWave(x, wave_params, wave):
    y = x.copy()

    for i in range(len(x)):
        y[i] = wave(wave_params[0], wave_params[1], wave_params[2], x[i])

    return y
