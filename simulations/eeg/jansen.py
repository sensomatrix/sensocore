# Maximum freq: 1000 Hz
# Minimum duration: 1 sec
# Usage: call simulate_eeg_jansen(parameters)
# Input parameters: duration, sampling frequency, C1, callback function
# Output: tuple with time and y arrays

from numpy import linspace, random, exp, asarray, dtype, around
from scipy.integrate import ode
from scipy.interpolate import interp1d


def sigmoid(v0, e0, r, v):
    sigm = (2 * e0) / (1 + exp(r * (v0 - v)))
    return sigm


def func(t, y, noise_interp, A, B, a, b, v0, C1, C2, C3, C4, r, e0):
    n = noise_interp(t)
    y1, y2, y3, y4, y5, y6 = y
    dy1dt = y4
    dy2dt = y5
    dy3dt = y6
    dy4dt = A * a * sigmoid(v0, e0, r, y2 - y3) - 2 * a * y4 - a * a * y1
    dy5dt = A * a * (n + C2 * sigmoid(v0, e0, r, C1 * y1)) - 2 * a * y5 - a * a * y2
    dy6dt = B * b * (C4 * sigmoid(v0, e0, r, C3 * y1)) - 2 * b * y6 - b * b * y3
    return [dy1dt, dy2dt, dy3dt, dy4dt, dy5dt, dy6dt]


def simulate_eeg_jansen(duration=10, fs=100, C1=135, callback=None):

    A = 3.25
    B = 22
    a = 100
    b = 50
    v0 = 6
    C2 = 0.8 * C1
    C3 = 0.25 * C1
    C4 = 0.25 * C1
    r = 0.56
    e0 = 2.5

    time_array = linspace(0, duration + 1, num=1 + fs * (duration + 1))
    noise = random.randint(120, high=320+1, size=time_array.size) #uniformly distributed white noise
    noise_interp = interp1d(time_array, noise, fill_value="extrapolate")  #noise interp function
    ode_time = []
    ode_y = []
    y0 = [0, 0, 0, 0, 0, 0]
    t0 = 0
    r = ode(func).set_integrator('dopri5', nsteps=10000, atol=1e-6, rtol=1e-3).set_f_params(noise_interp, A, B, a, b, v0, C1, C2, C3, C4, r, e0)
    r.set_initial_value(y0, t0)
    dt = 1 / fs
    while r.successful() and r.t < duration + 1:
        r.integrate(r.t + dt)
        ode_time.append(r.t)
        ode_y.append(r.y[1] - r.y[2])
        if callback is not None:
            callback(r.t/(duration+1)) #percentage of completion

    duration = int(duration)

    ode_time = ode_time[-(duration * fs + 1):] #remove the first second (we don't want the transient part)
    ode_y = ode_y[-(duration * fs + 1):]
    ode_time = asarray(ode_time, dtype=dtype(float))
    ode_time = ode_time - ode_time[0]
    ode_time = around(ode_time, 3)
    ode_y = asarray(ode_y, dtype=dtype(float))

    return ode_time, ode_y  # return a tuple with time and y.

