import numpy as np
def generateTimeArrayFromNumberOfSamples(samplingrate, numberOfSamples):
    time_array = np.true_divide(np.linspace(0, numberOfSamples - 1, numberOfSamples, dtype=np.float32), samplingrate)
    return time_array