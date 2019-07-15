# /src/views/views_helper.py
from ..models.signal import Signal, SignalSchema
from ..models.epoch import Epoch, EpochSchema
from ..models.data import Data, DataSchema

signal_schema = SignalSchema()
epoch_schema = EpochSchema()
data_schema = DataSchema()

def create_signals(signals_data, device_id=None):
    for signal_json in signals_data:
        signal_data, error = signal_schema.load(signal_json)
        if signal_data:
            signal = Signal(signal_data)
            signal.device_id = device_id
            signal.save()

            create_epochs(signal.id, signal_json['epochs'])
            create_data(signal.id, signal_json['data'])

def create_epochs(signal_id, epochs_data):
    for epoch_json in epochs_data:
        epoch_data, error = epoch_schema.load(epoch_json)
        if epoch_data:
            epoch = Epoch(epoch_data)
            epoch.signal_id = signal_id
            epoch.save()


def create_data(signal_id, data_serialized):
    data = Data(data_serialized)
    data.signal_id = signal_id
    data.save()
