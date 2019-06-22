#!venv/bin/python
from flask import Flask, jsonify

app = Flask(__name__)

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
def get_signals():
    return jsonify({'signals': signals})

from flask import abort

@app.route('/sensocore/api/v1.0/signals/<int:signal_id>', methods=['GET'])
def get_signal(signal_id):
    signal = [signal for signal in signals if signal['id'] == signal_id]
    if len(signal) == 0:
        abort(404)
    return jsonify({'signal': signal[0]})

if __name__ == '__main__':
    app.run(debug=True)