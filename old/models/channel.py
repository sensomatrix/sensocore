from utils.timeutils import generateTimeArrayFromNumberOfSamples, convert_start_and_end_time


class Channel:
    """object that stores each channel's info"""

    def __init__(self, name=None, fs=None, samples_array=None, channel_dimens=None, sensor=None, description=None,
                 unit=None, start_time=None, end_time=None, epochs=None):
        self.name = name
        self.fs = fs  # sampling rate
        self.samples_array = samples_array  # array of sample arrays
        self.channel_dimens = channel_dimens  # the num of dimensions ex: accelerometer has 3 signals x,y,z
        self.sensor = sensor
        self.description = description
        self.unit = unit  # unit of the signal ex: nW, BPM
        self.start_time, self.end_time = convert_start_and_end_time(start_time, end_time)
        self.epochs = epochs

        # time array based on fs for 1 dimension channel
        if not isinstance(fs, list) and fs != "_NaN_":
            self.time_array = generateTimeArrayFromNumberOfSamples(self.start_time,
                                                                   self.end_time,
                                                                   len(samples_array))

        # don't create time array for IBI(interbeat interval or RR interval)
        elif not isinstance(fs, list) and fs == "_NaN_":
            pass
        # array of time array based on fs for each dimension
        else:
            self.time_array = [generateTimeArrayFromNumberOfSamples(s, e, len(samples_array[i]))
                               for s, e, i in zip(self.start_time, self.end_time, range(len(fs)))]