import os
from itertools import islice
from models.signal import Signal
import numpy as np
from PyQt5.QtWidgets import QAction, QFileDialog
from PyQt5.QtCore import pyqtSignal, QObject
from models.channel import Channel
from models.epoch import Epoch
from models.patient import Patient
import re
import json


# dialog used to load a complete dataset. to do: deal with the case user clicks on "cancel"
def open_dataset_dialog(parent):
    openfilepath = QFileDialog.getOpenFileName(parent)
    if openfilepath[0]:
        return load_from_file(openfilepath[0])
        # for signal in signals:
        #     self.signal_loaded_signal.emit(sig)
        # self.parent.info.set_opened_filename(os.path.basename(openfilepath[0]))

def load_from_file(path_to_file):
    signals = []
    if re.search("\.json$", path_to_file):  # if json file
        signals = load_from_json(path_to_file)
        return signals

    with open(path_to_file, 'r') as fileObject:
        lines = readnextlines(fileObject, 5)
        while len(lines) == 5:
            name = lines[0]
            typeofsignal = lines[1]
            samplingrate = int(lines[2])
            time_array = (np.asarray(lines[3].split(", "))).astype(np.float32)
            samples_array = (np.asarray(lines[4].split(", "))).astype(np.float32)
            sig = Signal(samples_array, time_array=time_array, name=name, signal_type=typeofsignal, fs=samplingrate)
            signals.append(sig)
            lines = readnextlines(fileObject, 5)

    return signals

    # def loadFromSimulation(self, samples_array, time_array, fs, name, type):
    #     sig = Signal(samples_array, time_array=time_array, fs=fs, name=name, type=type)
    #     self.signals_dictionary[sig.id] = sig
    #     self.signal_loaded_signal.emit(sig)
    #
    # def addSignaltoDataset(self, signal):
    #     self.signals_dictionary[signal.id] = signal
    #     self.signal_loaded_signal.emit(signal)
    #
def readnextlines(fileObject, n):
    return [x.strip() for x in islice(fileObject, n)]
    #
    # def getSignalsList(self):
    #     return self.signals_dictionary
    #
    # def removeDC(self, id_):
    #     self.signals_dictionary.get(id_).removeDC()
    #     self.signal_changed_signal.emit(id_)
    #
    # def changeSamplesArray(self, id_, new_samples_array):
    #     self.signals_dictionary.get(id_).samples_array = new_samples_array
    #     self.signal_changed_signal.emit(id_)

def json_parser(filepath):
    """function that parses the json file and returns the data"""
    with open(filepath) as file:
        data = json.loads(file.read())
    head = list(data.keys())[0]  # the first key in json

    patient_id = data[head]['header']['patient_information']['id']
    age = data[head]['header']['patient_information']['age']
    address = data[head]['header']['patient_information']['address']
    bday = data[head]['header']['patient_information']['birthdate']
    sex = data[head]['header']['patient_information']['sex']
    instituition = data[head]['header']['recording_info']['instituition']
    date = data[head]['header']['recording_info']['date']
    visit_num = data[head]['header']['recording_info']['visit_num']
    device_name = data[head]['header']['device_information']['name']

    channel_keys = [x for x in list(data[head]['header']['device_information'].keys())
                         if re.search("^channel\d+", x)]  # ex: channel1, channel2

    channels = {}  # dictionary of channels ex: "channel1" = Channel object
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

        # epoch info
        epoch_keys = [x for x in list(data[head]['header']['epoch_information'][c].keys())
                        if re.search("^epoch\d+", x)]  # ex: epoch1, epoch2

        epochs = {}  # dictionary of epochs ex: "epoch1" = Epoch object
        for e in epoch_keys:
            epoch_name = data[head]['header']['epoch_information'][c][e]['name']
            epoch_start_time = data[head]['header']['epoch_information'][c][e]['start_time']
            epoch_end_time = data[head]['header']['epoch_information'][c][e]['end_time']
            epochs[e] = Epoch(epoch_name, epoch_start_time, epoch_end_time)
        channels[c] = Channel(name, fs, samples_array, channel_dimens, sensor, description, unit, start_time,
                              end_time, epochs)
    return Patient(patient_id, age, address, bday, sex, instituition, date, visit_num, device_name, channels)


def load_from_json(filepath):
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
                typeofsignal = c.sensor
                samplingrate = c.fs[s]
                time_array = (np.asarray(c.time_array[s])).astype(np.float32)
                samples_array = (np.asarray(c.samples_array[s])).astype(np.float32)
                sig = Signal(samples_array, time_array=time_array, name=name, signal_type=typeofsignal, fs=samplingrate)
                signals.append(sig)
        else:  # if single signal in 1 channel
            name = c.name
            typeofsignal = c.sensor
            samplingrate = c.fs
            time_array = (np.asarray(c.time_array)).astype(np.float32)
            samples_array = (np.asarray(c.samples_array)).astype(np.float32)
            sig = Signal(samples_array, time_array=time_array, name=name, signal_type=typeofsignal, fs=samplingrate)
            signals.append(sig)
    return signals
