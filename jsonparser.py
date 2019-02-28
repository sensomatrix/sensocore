import json
import re
from timeutils import generateTimeArrayFromNumberOfSamples


class JsonParser:
    """object that parses the json file and stores the data"""

    def __init__(self, filepath):
        with open(filepath) as file:
            self.data = json.loads(file.read())
            self.head = list(self.data.keys())[0] #the first key in json
            self.channel_keys = [x for x in list(self.data[self.head]['header']['device_information'].keys())
                                 if re.search("^channel\d+", x)]  # ex: channel1, channel2

            self.channels = {}  # dictionary of channels ex: "channel1" = Channel object
            for c in self.channel_keys:
                name = self.data[self.head]['header']['device_information'][c]['name']
                fs = self.data[self.head]['header']['device_information'][c]['data']['fs']
                samples_array = self.data[self.head]['Raw_Signal'][c]['data']
                channel_dimens = self.data[self.head]['header']['device_information'][c]['data']['dimension']
                sensor = self.data[self.head]['header']['device_information'][c]['sensor']
                description = self.data[self.head]['header']['device_information'][c]['data']['description']
                unit = self.data[self.head]['header']['device_information'][c]['data']['unit']
                self.channels[c] = Channel(name, fs, samples_array, channel_dimens, sensor, description, unit)


class Channel:
    """object that stores each channel's info"""

    def __init__(self, name=None, fs=None, samples_array=None, channel_dimens=None, sensor=None, description=None,
                 unit=None):
        self.name = name
        self.fs = fs  # sampling rate
        self.samples_array = samples_array  # array of sample arrays
        self.channel_dimens = channel_dimens  # the num of dimensions ex: accelerometer has 3 signals x,y,z
        self.sensor = sensor
        self.description = description
        self.unit = unit  # unit of the signal ex: nW, BPM
        # time array based on fs for 1 dimension channel
        if not isinstance(fs, list) and fs != "_NaN_":
            self.time_array = generateTimeArrayFromNumberOfSamples(fs, len(samples_array))
        # don't create time array for IBI(interbeat interval or RR interval)
        elif not isinstance(fs, list) and fs == "_NaN_":
            pass
        # array of time array based on fs for each dimension
        else:
            self.time_array = [generateTimeArrayFromNumberOfSamples(f, len(samples_array[i])) for f, i in zip(fs, range(len(fs)))
                               if f != "_NaN_"]


if __name__ == "__main__":

    path = "C:\\Users\\Ajevan\\Desktop\\ELEC 490\\JSON Files\\JSONFile_Raw.json"
    file = JsonParser(path)
    #print(file.data[file.head]['Raw_Signal']['channel1']['data'][0])
