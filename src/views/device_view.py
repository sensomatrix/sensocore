# /src/views/device_view.py
from flask import request, g, Blueprint, json, Response
from ..models.signal import Signal, SignalSchema
from ..models.device import Device, DeviceSchema
from numpy import mean, fromstring
from ..simulations.eeg import simulate_eeg_jansen
from ..simulations.ecg import generate_ecg
import json

device_api = Blueprint('device_api', __name__)
signal_schema = SignalSchema()
device_schema = DeviceSchema()


@signal_api.route('/', methods=['POST'])
def create():
    """
    Create Device Function
    """
    req_data = request.get_json()
    signal_data, error = signal_schema.load(req_data)

    check_for_error(error)

    actual_data, error = data_schema.load(req_data.get('data'))

    check_for_error(error)

    signal = Signal(signal_data)
    signal.save()

    actual_data['signal_id'] = signal.id
    data = Data(actual_data)
    data.save()

    epochs = []

    for epoch in req_data.get('epochs'):
        actual_epoch, error = epoch_schema.load(epoch)

        check_for_error(error)

        actual_epoch['signal_id'] = signal.id
        epoch = Epoch(actual_epoch)
        epoch.save()
        epochs.append(epoch)

    signal.data = data
    signal.epochs = epochs
    signal.save()

    data = signal_schema.dump(signal).data
    return custom_response(data, 201)


@signal_api.route('/sim', methods=['POST'])
def create_simulation():
    """
    Creating a simulated signal
    """
    req_data = request.get_json()
    type = req_data.pop('type', None)
    if type == 'ECG':
        # ecg = generate_ecg(**req_data)
        pass
    elif type == 'EEG':
        eeg = simulate_eeg_jansen(**req_data)

    return custom_response("{}", 200)


@signal_api.route('/', methods=['GET'])
def get_all():
    """
    Get All Signals
    """
    signals = Signal.get_all_signals()
    data = signal_schema.dump(signals, many=True).data
    return custom_response(data, 200)


@signal_api.route('/<int:signal_id>', methods=['GET'])
def get_one(signal_id):
    """
    Get A Signal
    """
    signal = Signal.get_one_signal(signal_id)
    if not signal:
        return custom_response({'error': 'signal not found'}, 404)
    data = signal_schema.dump(signal).data
    return custom_response(data, 200)


@signal_api.route('/<int:signal_id>', methods=['PUT'])
def update(signal_id):
    """
    Update A Signal
    """
    req_data = request.get_json()
    signal = Signal.get_one_signal(signal_id)
    if not signal:
        return custom_response({'error': 'signal not found'}, 404)
    data = signal_schema.dump(signal).data
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    data, error = signal_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)
    signal.update(data)

    data = signal_schema.dump(signal).data
    return custom_response(data, 200)


@signal_api.route('/<int:signal_id>', methods=['DELETE'])
def delete(signal_id):
    """
    Delete A Signal
    """
    signal = Signal.get_one_signal(signal_id)
    if not signal:
        return custom_response({'error': 'signal not found'}, 404)
    data = signal_schema.dump(signal).data
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    signal.delete()
    return custom_response({'message': 'deleted'}, 204)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )


def check_for_error(error):
    if error:
        return custom_response(error, 400)
