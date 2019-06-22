#!venv/bin/python
from flask import Flask, jsonify

app = Flask(__name__)

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'niroigen':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

signals = [
    {
        'id': 1,
        'name': 'ECG Signal',
        'fs': 255, 
        'type': 'ECG',
        'unit': 'mV',
        'time_array': [0,1,2,3,4,5,6,7,8],
        'raw': [0.1,0.3,0.1, 0.5, 0.1, 0.2, 0.5, 0.1, 0.2]
    },
    {
        'id': 2,
        'name': 'EEG Signal',
        'fs': 250, 
        'type': 'EEG',
        'unit': 'mV',
        'time_array': [0,1,2,3,4,5,6,7,8],
        'raw': [0.1,-0.3,0.1, 0.5, -0.1, -0.2, 0.5, 0.1, 0.2]
    }
]

@app.route('/sensocore/api/v1.0/signals', methods=['GET'])
@auth.login_required
def get_signals():
    return jsonify({'signals': [make_public_signal(signal) for signal in signals]})

from flask import abort

@app.route('/sensocore/api/v1.0/signals/<int:signal_id>', methods=['GET'])
@auth.login_required
def get_signal(signal_id):
    signal = [signal for signal in signals if signal['id'] == signal_id]
    if len(signal) == 0:
        abort(404)
    return jsonify({'signal': signal[0]})

from flask import make_response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

from flask import request

@app.route('/sensocore/api/v1.0/signals', methods=['POST'])
@auth.login_required
def create_signal():
    if not request.json or not 'name' in request.json:
        abort(400)
    signal = {
        'id': signals[-1]['id'] + 1,
        'name': request.json['name'],
        'fs': request.json['fs'],
        'type': request.json['type'],
        'unit': request.json['unit'],
        'time_array': request.json['time_array'],
        'raw': request.json['raw']
    }
    signals.append(signal)
    return jsonify({'signal': signal}), 201

@app.route('/sensocore/api/v1.0/signals/<int:signal_id>', methods=['PUT'])
@auth.login_required
def update_signal(signal_id):
    signal = [signal for signal in signals if signal['id'] == signal_id]
    if len(signal) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'fs' in request.json and type(request.json['fs']) is not float:
        abort(400)
    signal[0]['name'] = request.json.get('name', signal[0]['name'])
    signal[0]['type'] = request.json.get('type', signal[0]['type']),
    signal[0]['unit'] = request.json.get('unit', signal[0]['unit']),
    signal[0]['time_array'] = request.json.get('time_array', signal[0]['time_array']),
    signal[0]['raw'] = request.json.get('raw', signal[0]['raw']),

    return jsonify({'signal': signal[0]})

@app.route('/sensocore/api/v1.0/signals/<int:signal_id>', methods=['DELETE'])
@auth.login_required
def delete_signal(signal_id):
    signal = [signal for signal in signals if signal['id'] == signal_id]
    if len(signal) == 0:
        abort(404)
    signals.remove(signal[0])
    return jsonify({'result': True})


from flask import url_for

def make_public_signal(signal):
    new_signal = {}
    for field in signal:
        if field == 'id':
            new_signal['uri'] = url_for('get_signal', signal_id=signal['id'], _external=True)
        else:
            new_signal[field] = signal[field]
    return new_signal

if __name__ == '__main__':
    app.run(debug=True)