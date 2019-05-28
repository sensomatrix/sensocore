import pyedflib


def write_edf(signals, filename):
    channel_info = []
    data_list = []

    f = pyedflib.EdfWriter(filename, len(signals))

    for signal in signals:
        ch_dict = {'label': signal.name, 'dimension': signal.unit, 'sample_rate': signal.fs, 'physical_max': 100, 'physical_min': -100, 'digital_max': 32767, 'digital_min': -32768, 'transducer': '', 'prefilter':''}
        channel_info.append(ch_dict)
        data_list.append(signal.raw)

    f.setSignalHeaders(channel_info)
    f.writeSamples(data_list)
    f.close()
    del f
