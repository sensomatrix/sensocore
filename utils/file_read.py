import os
from itertools import islice
from models.signal import Signal
import numpy as np
from PyQt5.QtWidgets import QAction, QFileDialog
from models.channel import Channel
from models.epoch import Epoch
from models.patient import Patient
from PyQt5.QtCore import pyqtSignal, QObject
from pathlib import Path
import mne
import json
import re
import bioread


# dialog used to load a complete dataset. to do: deal with the case user clicks on "cancel"
def open_dataset_dialog(parent):
    home = str(Path.home())
    dir = os.path.join(home, 'Bio Signals')

    if not os.path.exists(dir):
        os.makedirs(dir)

    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName(parent, 'Select a folder:', dir,
                                              "All Files (*)", options=options)

    if fileName != '':
        return load_from_file(fileName, parent)
        # for signal in signals:
        #     self.signal_loaded_signal.emit(sig)
        # self.parent.info.set_opened_filename(os.path.basename(openfilepath[0]))

def load_from_file(path_to_file, parent):
    signals = []
    if re.search("\.json$", path_to_file):  # if json file
        signals = load_from_json(path_to_file, parent)
        return signals
    elif re.search("\.fif$", path_to_file):
        signals = load_from_fif(path_to_file)
        return signals
    elif re.search("\.edf$", path_to_file):
        signals = load_from_edf(path_to_file)
        return signals
    elif re.search("\.acq$", path_to_file):
        signals = load_from_acq(path_to_file)
        return signals
    # if re.search("\.edf", path_to_file):
    #     signals = load_from_edf(path_to_file)
    #     return signals
    with open(path_to_file, 'r') as fileObject:
        lines = readnextlines(fileObject, 5)
        while len(lines) == 5:
            name = lines[0]
            typeofsignal = lines[1]
            samplingrate = int(lines[2])
            time_array = (np.asarray(lines[3].split(", "))).astype(np.float32)
            samples_array = (np.asarray(lines[4].split(", "))).astype(np.float32)

            time_array = np.reshape(time_array, (time_array.shape[0], 1))
            samples_array = np.reshape(samples_array, (samples_array.shape[0], 1))

            signal = np.hstack([time_array, samples_array])

            sig = Signal(signal, name=name, signal_type=typeofsignal, fs=samplingrate)
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
            epochs[e] = Epoch(epoch_name, epoch_start_time, epoch_end_time)
        channels[c] = Channel(name, fs, samples_array, channel_dimens, sensor, description, unit, start_time,
                              end_time, epochs)

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

def load_from_fif(filename):
    signals = []
    raw = mne.io.read_raw_fif(filename)

    picks = mne.pick_types(raw.info, meg=False, eeg=True)
    t_idx = raw.time_as_index([0., 30.])

    data, times = raw[picks, t_idx[0]:t_idx[1]]

    for idx, pick in enumerate(picks):
        name = raw.ch_names[pick]
        typeofsignal = 'EEG'
        samplingrate = raw.info['sfreq']
        time_array = times
        samples_array = data[idx]
        signal = np.hstack(
            [time_array.reshape((time_array.shape[0], 1)), samples_array.reshape((samples_array.shape[0], 1))])
        sig = Signal(signal, name=name, signal_type=typeofsignal, fs=samplingrate)
        signals.append(sig)

    return signals


def load_from_edf(filename, sample_from=-1, sample_to=-1):
    raw = mne.io.read_raw_edf(filename, preload=True)
    picks = mne.pick_channels(raw.ch_names, [], exclude=['COUNTER', 'INTERPOLATED', 'MARKER', 'MARKER_HARDWARE', 'SYNC',
                                                     'TIME_STAMP_s', 'TIME_STAMP_ms', 'CQ_AF3', 'CQ_T7', 'CQ_Pz',
                                                     'CQ_T8', 'RAW_CQ', 'GYROX', 'GYROY', 'STI 014']) 

    if sample_from != -1 and sample_to != -1:
        start_time = sample_from / raw.info['sfreq']
        end_time = sample_to / raw.info['sfreq']

        t_idx = raw.time_as_index([start_time, end_time])

        data, times = raw[picks, t_idx[0]:t_idx[1]]

    else:
        data, times = raw[picks, :]

    signals = []

    for samples, channel_index in zip(data, picks):
        name = raw.ch_names[channel_index]
        typeofsignal = ''
        samplingrate = raw.info['sfreq']
        time_array = times
        samples_array = samples
        signal = np.hstack(
            [time_array.reshape((time_array.shape[0], 1)), samples_array.reshape((samples_array.shape[0], 1))])
        epochs = None
        sig = Signal(signal, name=name, signal_type=typeofsignal, fs=samplingrate, epochs=epochs)
        signals.append(sig)

    return signals

def load_from_acq(filename):
    data = bioread.read_file(filename)

    signals = []

    for channel in data.channels:
        name = channel.name
        typeofsignal = ''
        samplingrate = channel.samples_per_second
        time_array = channel.time_index
        samples_array = channel.data

        min = -10000
        max = 10000

        for index, data in enumerate(samples_array):
            if data > max:
                samples_array[index] = max
            if data < min:
                samples_array[index] = min            

        signal = np.hstack(
            [time_array.reshape((time_array.shape[0], 1)), samples_array.reshape((samples_array.shape[0], 1))])
        units = channel.units
        sig = Signal(signal, name=name, signal_type=typeofsignal, fs=samplingrate, unit=units)
        signals.append(sig)

    return signals


def convert_to_string(numstring):
    if isinstance(numstring, list):
       numstring = [str(e) for e in numstring]
    else:
        numstring = str(numstring)
    return numstring
