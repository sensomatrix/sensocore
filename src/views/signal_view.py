# /src/views/SignalView.py
from flask import request, g, Blueprint, json, Response
from src.models.signal import Signal, SignalSchema
from src.models.data import Data, DataSchema
from src.models.epoch import Epoch, EpochSchema
from src.views.views_helper import create_data, create_epochs
from numpy import mean, fromstring
from src.simulations.ecg import generate_ecg
import json

signal_api = Blueprint('signal_api', __name__)
signal_schema = SignalSchema()
data_schema = DataSchema()
epoch_schema = EpochSchema()


@signal_api.route('/', methods=['POST'])
def create():
    """
    Create Signal Function
    """
    req_data = request.get_json()
    signal_data, error = signal_schema.load(req_data)

    if error:
        return custom_response(error, 400)

    signal = Signal(signal_data)
    signal.save()

    create_epochs(signal.id, req_data['epochs'])
    create_data(signal.id, req_data['data'])

    data = signal_schema.dump(signal).data
    return custom_response(data, 201)


@signal_api.route('/simulate/ecg', methods=['POST'])
def simulate_ecg():
    """
    Simulate an ecg signal
    """
    req_data = request.get_json()
    ecg_sim = generate_ecg(**req_data)
    signal_data, error = signal_schema.load({
        "name": "ECG Simulated Signal",
        "raw": ecg_sim,
    })

    if error:
        return custom_response(error, 400)

    signal = Signal(signal_data)
    signal.save()

    create_data(signal.id, {
        "channel_num": 1,
        "description": "Simulated ECG Signal",
        "start_time": "15:00:00",  # TODO: Change this
        "end_time": "16:00:00",  # TODO: Change this
        "duration": req_data['duration'],
        "fs": req_data['fs'],
        "unit": "mV"
    })

    data = signal_schema.dump(signal).data
    return custom_response(data, 201)


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
