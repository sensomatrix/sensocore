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
