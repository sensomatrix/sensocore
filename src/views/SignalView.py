# /src/views/SignalView.py
from flask import request, g, Blueprint, json, Response
from ..models.signal import Signal, SignalSchema
from ..models.data import Data, DataSchema
from numpy import mean, fromstring
from ..simulations.eeg import simulate_eeg_jansen
from ..simulations.ecg import generate_ecg 
import json

signal_api = Blueprint('signal_api', __name__)
signal_schema = SignalSchema()
data_schema = DataSchema()


@signal_api.route('/', methods=['POST'])
def create():
    """
    Create Signal Function
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

    signal.data = data
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


@signal_api.route('/remove-dc/<int:signal_id>', methods=['PUT'])
def remove_dc(signal_id):
    """
    Removes the DC of a signal
    """
    req_data = request.get_json()

    signal = Signal.get_one_signal(signal_id)
    signal_json = json.loads(signal_schema.dump(signal).data['data'])
    data = signal_json[req_data['mode']][req_data['channel']]['data']
    mean_value = data - mean(data)
    data = str(mean_value.tolist())
    signal_json[req_data['mode']][req_data['channel']]['data'] = data

    signal.data = json.dumps(signal_json)
    signal.save()

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