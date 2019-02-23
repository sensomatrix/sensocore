import numpy as np
from functools import reduce
def generateTimeArrayFromNumberOfSamples(samplingrate, numberOfSamples):
    time_array = np.true_divide(np.linspace(0, numberOfSamples - 1, numberOfSamples, dtype=np.float32), samplingrate)
    return time_array

def secondsToHHMMSSMMM(t):
    return "%02d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])
