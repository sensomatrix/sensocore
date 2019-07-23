# /src/views/patient_view.py
from flask import request, g, Blueprint, json, Response
from src.models.signal import Signal, SignalSchema
from src.models.device import Device, DeviceSchema
from src.models.patient import Patient, PatientSchema
from src.models.recording import Recording, RecordingSchema
from src.views.views_helper import create_signals
import json
from src.shared.file_read import json_parser

patient_api = Blueprint('patient_api', __name__)
signal_schema = SignalSchema()
device_schema = DeviceSchema()
patient_schema = PatientSchema()
recording_schema = RecordingSchema()

@patient_api.route('/upload', methods=['POST'])
def upload():
    """
    Upload a patient
    """
    file = json.loads(request.files['file'].read())
    head = list(file.keys())[0]
    patient_info = file[head]['header']['patient_information']
    recording_info = file[head]['header']['recording_info']
    patient_data, error = patient_schema.load(patient_info)
    
    if (error):
        return custom_response(error, 400)
    recording_data, error = recording_schema.load(recording_info)

    if (error):
        return custom_response(error, 400)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
