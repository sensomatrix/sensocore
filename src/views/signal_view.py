# /src/views/SignalView.py
from flask import request, g, Blueprint, json, Response
from src.models.signal import Signal, SignalSchema
from src.models.data import Data, DataSchema
from src.models.epoch import Epoch, EpochSchema
from src.views.views_helper import create_data, create_epochs
from numpy import mean, fromstring
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

    signal = Signal(signal_data)
    signal.save()

    create_epochs(signal.id, signal_data['epochs'])
    create_data(signal.id, signal_data['data'])

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

def check_for_error(error):
    if error:
        return custom_response(error, 400)