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
  post = SignalModel(data)
  post.save()
  data = signal_schema.dump(post).data
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
