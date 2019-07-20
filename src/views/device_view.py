# /src/views/device_view.py
from flask import request, g, Blueprint, json, Response
from src.models.signal import Signal, SignalSchema
from src.models.device import Device, DeviceSchema
from src.views.views_helper import create_signals
import json

device_api = Blueprint('device_api', __name__)
signal_schema = SignalSchema()
device_schema = DeviceSchema()


@device_api.route('/', methods=['POST'])
def create():
    """
    Create Device Function
    """
    req_data = request.get_json()
    device_data, error = device_schema.load(req_data)

    if error:
        return custom_response(error, 400)

    device = Device(device_data)
    device.save()

    create_signals(req_data['signals'], device.id)

    data = device_schema.dump(device).data
    return custom_response(data, 201)


@device_api.route('/', methods=['GET'])
def get_all():
    """
    Get All Devices
    """
    devices = Device.get_all_devices()
    data = device_schema.dump(devices, many=True).data
    return custom_response(data, 200)


@device_api.route('/<int:device_id>', methods=['GET'])
def get_one(device_id):
    """
    Get A Device
    """
    device = Device.get_one_device(device_id)
    if not device:
        return custom_response({'error': 'device not found'}, 404)
    data = device_schema.dump(device).data
    return custom_response(data, 200)


@device_api.route('/<int:device_id>', methods=['PUT'])
def update(device_id):
    """
    Update A Device
    """
    req_data = request.get_json()
    device = Device.get_one_device(device_id)
    if not device:
        return custom_response({'error': 'device not found'}, 404)

    data, error = device_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)

    device.update(data)

    data = device_schema.dump(device).data
    return custom_response(data, 200)

@device_api.route('/<int:device_id>', methods=['DELETE'])
def delete(device_id):
    """
    Delete A device
    """
    device = Device.get_one_device(device_id)
    if not device:
        return custom_response({'error': 'device not found'}, 404)

    device.delete()
    return custom_response({}, 204)

def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
