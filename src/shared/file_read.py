import os
from itertools import islice
import numpy as np
from pathlib import Path
import json
import re
from src.models.patient import Patient

def load_channels(data):
    head = list(data.keys())[0]  # the first key in json
    channel_keys = [x for x in list(data[head]['header']['device_information'].keys())
                            if re.search("^channel\d+", x)]  # ex: channel1, channel2

    channels = {}  # dictionary of channels ex: "channel1" = Channel object
    channel_info_dict = {}
    for c in channel_keys:
        # device info
        name = data[head]['header']['device_information'][c]['name']
        fs = data[head]['header']['device_information'][c]['data']['fs']
        samples_array = data[head]['Raw_Signal'][c]['data']
        channel_dimens = data[head]['header']['device_information'][c]['data']['dimension']
        sensor = data[head]['header']['device_information'][c]['sensor']
        description = data[head]['header']['device_information'][c]['data']['description']
        unit = data[head]['header']['device_information'][c]['data']['unit']
        start_time = data[head]['header']['device_information'][c]['data']['start_time']
        end_time = data[head]['header']['device_information'][c]['data']['end_time']

        if name != "IBI":
            channel_info_dict.update({c: ['Name: '+name, {'fs': convert_to_string(fs)},
                                        'Channel dimensions: '+convert_to_string(channel_dimens),
                                        {'Sensor': sensor}, {'Description': description}]})

        # epoch info
        epoch_keys = [x for x in list(data[head]['header']['epoch_information'][c].keys())
                        if re.search("^epoch\d+", x)]  # ex: epoch1, epoch2

        epochs = {}  # dictionary of epochs ex: "epoch1" = Epoch object
        for e in epoch_keys:
            epoch_name = data[head]['header']['epoch_information'][c][e]['name']
            epoch_start_time = data[head]['header']['epoch_information'][c][e]['start_time']
            epoch_end_time = data[head]['header']['epoch_information'][c][e]['end_time']
            epochs[e] = {'epoch_name': epoch_name,
            'epoch_start_time': epoch_start_time,
            'epoch_end_time': epoch_end_time}

    return channel_info_dict, epochs

def json_parser(data):
    """
    Function that parses the json file and returns the data
    """
    head = list(data.keys())[0]  # the first key in json
    patient_info = {}

    patient_id = data[head]['header']['patient_information']['id']
    age = data[head]['header']['patient_information']['age']
    address = data[head]['header']['patient_information']['address']
    bday = data[head]['header']['patient_information']['birthdate']
    sex = data[head]['header']['patient_information']['sex']
    instituition = data[head]['header']['recording_info']['instituition']
    date = data[head]['header']['recording_info']['date']
    visit_num = data[head]['header']['recording_info']['visit_num']
    device_name = data[head]['header']['device_information']['name']

    patient_info.update({'Patient Information': ['ID: '+str(patient_id), 'Age: '+str(age), 'Address: '+str(address),
                                                 'Birth date: '+bday, 'Sex: '+sex]})
    patient_info.update({'Recording Information': ['Institution: '+instituition, 'Date: '+date,
                                                   'Visit Number: '+str(visit_num)]})

    channels, channel_info_dict = load_channels(data)

    patient_info.update({'Device Information': ['Name: '+device_name, {'Channels': channel_info_dict}]})
    patient_info = {'File path: '+filepath: patient_info}
    return Patient(patient_id, age, address, bday, sex, instituition, date, visit_num, device_name,
                   channels, patient_info)

def load_from_json(filepath, parent):
    signals = []
    patient = json_parser(filepath)
    for c in patient.channels.values():
        # IBI interbeat interval skip for now
        if c.name == "IBI":
            continue
        # if multiple signals in 1 channel
        if isinstance(c.fs, list):
            for s in range(len(c.fs)):
                name = c.name
                unit = c.unit[s]
                typeofsignal = c.sensor
                samplingrate = c.fs[s]
                time_array = (np.asarray(c.time_array[s])).astype(np.float32)
                samples_array = (np.asarray(c.samples_array[s])).astype(np.float32)
                signal = np.hstack([time_array.reshape((time_array.shape[0], 1)), samples_array.reshape((samples_array.shape[0], 1))])
                epochs = c.epochs
                sig = Signal(signal, name=name, signal_type=typeofsignal, fs=samplingrate, epochs=epochs, unit=unit)
                signals.append(sig)
        else:  # if single signal in 1 channel
            name = c.name
            unit = c.unit
            typeofsignal = c.sensor
            samplingrate = c.fs
            samples = len(c.time_array)
            time_array = (np.asarray(c.time_array)).astype(np.float32).reshape((samples, 1))
            samples_array = (np.asarray(c.samples_array)).astype(np.float32).reshape((samples, 1))
            epochs = c.epochs
            signal = np.hstack([time_array, samples_array])
            sig = Signal(signal, name=name, signal_type=typeofsignal, fs=samplingrate, epochs=epochs, unit=unit)
            signals.append(sig)
    parent.patients.append_patient(patient)
    return signals

def convert_to_string(numstring):
    if isinstance(numstring, list):
       numstring = [str(e) for e in numstring]
    else:
        numstring = str(numstring)
    return numstring