#/src/views/BlogpostView.py
from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.SignalModel import SignalModel, SignalSchema

signal_api = Blueprint('signal_api', __name__)
signal_schema = SignalSchema()


@signal_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create Signal Function
  """
  req_data = request.get_json()
  req_data['owner_id'] = g.user.get('id')
  data, error = signal_schema.load(req_data)
  if error:
    return custom_response(error, 400)
  signal = SignalModel(data)
  signal.save()
  data = signal_schema.dump(post).data
  return custom_response(data, 201)

@signal_api.route('/', methods=['GET'])
def get_all():
  """
  Get All Signals
  """
  signals = SignalModel.get_all_signals()
  data = signal_schema.dump(signals, many=True).data
  return custom_response(data, 200)

@signal_api.route('/<int:signal_id>', methods=['GET'])
def get_one(signal_id):
  """
  Get A Signal
  """
  signal = SignalModel.get_one_signal(signal_id)
  if not signal:
    return custom_response({'error': 'signal not found'}, 404)
  data = signal_schema.dump(signal).data
  return custom_response(data, 200)

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
