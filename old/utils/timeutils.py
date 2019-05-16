import numpy as np
from functools import reduce
import time
import datetime


def generateTimeArrayFromNumberOfSamples(start_time, end_time, numberOfSamples):
    time_array = np.linspace(start_time, end_time, numberOfSamples, dtype=np.float32)
    return time_array


def generate_time_array(start_time, samples, fs):
    start = time_str_to_int(start_time)
    time_array = np.linspace(start, start + (samples/ fs), samples, dtype=np.float32)
    return time_array


def convert_start_and_end_time(s, e):
    if s is None and e is None:
        return s, e

    if isinstance(s, list):
        start_time = []
        end_time = []
        for s_time in s:
            start_time.append(time_str_to_int(s_time))
        for e_time in e:
            end_time.append(time_str_to_int(e_time))
    else:
        start_time = time_str_to_int(s)
        end_time = time_str_to_int(e)

    return start_time, end_time


def time_str_to_int(time_str):
    try:
        t = time.strptime(time_str, '%H:%M:%S')
        return int(datetime.timedelta(hours=t.tm_hour, minutes=t.tm_min, seconds=t.tm_sec).total_seconds())
    except:
        t = time.strptime(time_str, '%H:%M:%S.%f')
        # TODO: Figure out a way to include the milliseconds
        return int(datetime.timedelta(hours=t.tm_hour, minutes=t.tm_min, seconds=t.tm_sec).total_seconds())


def secondsToHHMMSSMMM(t):
    return "%02d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])
