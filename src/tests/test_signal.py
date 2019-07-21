import unittest
import os
import json
from src.app import create_app, db
from marshmallow import ValidationError
from src.models.signal import Signal, SignalSchema
from src.views.views_helper import create_data, create_epochs


class SignalModelTest(unittest.TestCase):
    """
    Signal Model Test Case
    """

    def setUp(self):
        """
        Test Setup
        """
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.signal_schema = SignalSchema()
        self.test_data = {
            "name": "test",
            "raw": [
                    1,
                    2,
                    3,
                    4
            ],
            "sensor": "Niro Device",
            "sensor_location_on_body": "arm",
            "data": {
                "channel_num": 1,
                "description": "test description",
                "start_time": "15:00:00",
                "end_time": "18:00:00",
                "duration": 180,
                "fs": 256,
                "unit": "mV"
            },
            "epochs": [
                {
                    "name": "Watching movie",
                    "start_time": "15:00:00",
                    "end_time": "15:30:00",
                    "duration": 30
                },
                {
                    "name": "Finishing movie",
                    "start_time": "16:00:00",
                    "end_time": "16:15:00",
                    "duration": 15
                }
            ]
        }

        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_display_signal_none(self):
        """ Test Display signal using repr"""
        signal_data, _ = self.signal_schema.load(self.test_data)

        signal = Signal(signal_data)
        self.assertEqual(repr(signal), '<id None>')

    def tearDown(self):
        """
        Tear Down
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


class SignalViewTest(unittest.TestCase):
    """
    Signal View Test Case
    """

    def setUp(self):
        """
        Test Setup
        """
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.test_data = {
            "name": "test",
            "raw": [
                    1,
                    2,
                    3,
                    4
            ],
            "sensor": "Niro Device",
            "sensor_location_on_body": "arm",
            "data": {
                "channel_num": 1,
                "description": "test description",
                "start_time": "15:00:00",
                "end_time": "18:00:00",
                "duration": 180,
                "fs": 256,
                "unit": "mV"
            },
            "epochs": [
                {
                    "name": "Watching movie",
                    "start_time": "15:00:00",
                    "end_time": "15:30:00",
                    "duration": 30
                },
                {
                    "name": "Finishing movie",
                    "start_time": "16:00:00",
                    "end_time": "16:15:00",
                    "duration": 15
                }
            ]
        }

        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_create_signal(self):
        """ Test Create Signal """
        res = self.client.post(
            '/api/v1/signals/', data=json.dumps(self.test_data), content_type='application/json')
        self.assertEqual(res.status_code, 201)

    def test_create_signal_error(self):
        """ Test Create Signal with invalid data """
        res = self.client.post(
            '/api/v1/signals/', data=json.dumps({}), content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_get_signals(self):
        """ Test Get Signals """
        res = self.client.post(
            '/api/v1/signals/', data=json.dumps(self.test_data), content_type='application/json')
        self.assertEqual(res.status_code, 201)

        res = self.client.get('/api/v1/signals/',
                              content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(res.status_code, 200)

    def test_get_signal(self):
        """Test Get One Signal"""
        res = self.client.post(
            '/api/v1/signals/', data=json.dumps(self.test_data), content_type='application/json')
        self.assertEqual(res.status_code, 201)

        res = self.client.get('/api/v1/signals/1',
                              content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_get_signal_error(self):
        """Test Attempt to get one signal that does not exist"""
        res = self.client.get('/api/v1/signals/1',
                              content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_update_signal_nonexistant(self):
        """Test Update a signal that does not exist"""
        res = self.client.put('/api/v1/signals/3', data=json.dumps({}),
                              content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_update_signal(self):
        """Test Update an existing signal"""
        res = self.client.post(
            '/api/v1/signals/', data=json.dumps(self.test_data), content_type='application/json')
        self.assertEqual(res.status_code, 201)

        new_name = 'Updated ECG Signal'
        res = self.client.put('/api/v1/signals/1', data=json.dumps({"name": new_name}),
                              content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(data['name'], new_name)
        self.assertEqual(res.status_code, 200)

    def test_update_data_of_signal(self):
        """Test Update data of a signal"""
        res = self.client.post(
            '/api/v1/signals/', data=json.dumps(self.test_data), content_type='application/json')
        self.assertEqual(res.status_code, 201)

        new_description = 'New Description'
        res = self.client.put('/api/v1/signals/1', data=json.dumps({"data": {
            "description": new_description
        }}),
            content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(data, {'description': new_description})
        self.assertEqual(res.status_code, 200)

    def test_update_data_of_signal_error(self):
        """Test Update data of a signal with error"""
        res = self.client.post(
            '/api/v1/signals/', data=json.dumps(self.test_data), content_type='application/json')
        self.assertEqual(res.status_code, 201)

        new_description = 'New Description'
        res = self.client.put('/api/v1/signals/1', data=json.dumps({"data": {
            'invalid': 'invalid'
        }}),
            content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data, {'invalid': ['Unknown field']})

    def test_update_epoch_of_signal_error(self):
        """Test Update epoch of a signal with error"""
        res = self.client.post(
            '/api/v1/signals/', data=json.dumps(self.test_data), content_type='application/json')
        self.assertEqual(res.status_code, 201)

        res = self.client.put('/api/v1/signals/1', data=json.dumps({
            "epoch": {
                "invalid": 'invalid',
            },
            'epoch_id': 1}), content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data, {'invalid': ['Unknown field']})

    def test_update_epoch_of_signal(self):
        """Test Update epoch of a signal"""
        res = self.client.post(
            '/api/v1/signals/', data=json.dumps(self.test_data), content_type='application/json')
        self.assertEqual(res.status_code, 201)

        new_name = 'New name'
        res = self.client.put('/api/v1/signals/1', data=json.dumps({
            "epoch": {
                "name": new_name,
            },
            'epoch_id': 1
        }), content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(data, {'name': new_name})
        self.assertEqual(res.status_code, 200)

    def test_update_signal_load_error(self):
        """Test Attempt to update an existing signal"""
        res = self.client.post(
            '/api/v1/signals/', data=json.dumps(self.test_data), content_type='application/json')
        self.assertEqual(res.status_code, 201)

        res = self.client.put('/api/v1/signals/1', data=json.dumps({"inavlid": "invalid"}),
                              content_type='application/json')
        self.assertRaises(ValidationError)
        self.assertEqual(res.status_code, 400)

    def test_delete_signal(self):
        """Test Delete a signal"""
        res = self.client.post(
            '/api/v1/signals/', data=json.dumps(self.test_data), content_type='application/json')
        self.assertEqual(res.status_code, 201)

        res = self.client.delete(
            '/api/v1/signals/1', content_type='application/json')
        self.assertEqual(res.status_code, 204)

    def test_delete_signal_nonexistant(self):
        """Test Delete a signal non existant"""
        res = self.client.delete(
            '/api/v1/signals/1', content_type='application/json')
        self.assertEqual(res.status_code, 404)
        self.assertEqual({'error': 'signal not found'}, json.loads(res.data))

    def test_simulate_ecg(self):
        """Test Simulate ECG"""
        duration = 200
        period = 1
        fs = 256
        res = self.client.post('api/v1/signals/simulate/ecg', data=json.dumps({
            "fs": fs,
            "noise_magnitude": 0,
            "duration": duration,
            "period": period,
            "delay": 0,
            "P": [
                0.180,
                0.2922,
                0.0178
            ],
            "Q": [
                -0.0223,
                0.3218,
                0.03064,
                -0.2725,
                0.37123,
                0.00571
            ],
            "R": [
                0.095,
                0.44471,
                0.01997
            ],
            "S": [
                0.179,
                0.46,
                0.009
            ],
            "T": [
                0.3255,
                0.654,
                0.02978
            ]
        }), content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(data['sensor'], None)
        self.assertEqual(data['sensor_location_on_body'], None)
        self.assertEqual(len(data['raw']), period * fs * duration)
        self.assertEqual(data['raw'][0:fs - 1], data['raw'][fs: 2*fs - 1])
        self.assertEqual(res.status_code, 201)

    def test_simulate_eeg(self):
        """Test Simulate EEG"""
        duration = 10
        fs = 1000
        c1 = 1350
        noise_magnitude = 0
        res = self.client.post('api/v1/signals/simulate/eeg', data=json.dumps({
            "fs": fs,
            "noise_magnitude": noise_magnitude,
            "duration": duration,
            'c1': c1
        }), content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(data['sensor'], None)
        self.assertEqual(data['sensor_location_on_body'], None)
        self.assertEqual(len(data['raw']), fs * duration + 1)
        self.assertEqual(res.status_code, 201)

    def test_simulate_eeg_error(self):
        """Test Simulate EEG with error"""
        res = self.client.post('api/v1/signals/simulate/eeg',
                               data=json.dumps({}), content_type='application/json')
        error = json.loads(res.data)
        self.assertEqual(error, {"error": [
                         "simulate_eeg_jansen() missing 4 required positional arguments: 'duration', 'fs', 'c1', and 'noise_magnitude'"]})
        self.assertEqual(res.status_code, 400)

    def test_simulate_ecg_less_than_one_beat(self):
        """Test Simulate ECG that is less than its period, 
        it should create a signal that is one beat lone"""
        duration = 0.5
        period = 1
        fs = 256
        res = self.client.post('api/v1/signals/simulate/ecg', data=json.dumps({
            "fs": fs,
            "noise_magnitude": 0,
            "duration": duration,
            "period": period,
            "delay": 0,
            "P": [
                0.180,
                0.2922,
                0.0178
            ],
            "Q": [
                -0.0223,
                0.3218,
                0.03064,
                -0.2725,
                0.37123,
                0.00571
            ],
            "R": [
                0.095,
                0.44471,
                0.01997
            ],
            "S": [
                0.179,
                0.46,
                0.009
            ],
            "T": [
                0.3255,
                0.654,
                0.02978
            ]
        }), content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(data['sensor'], None)
        self.assertEqual(data['sensor_location_on_body'], None)
        self.assertEqual(len(data['raw']), 256)
        self.assertEqual(res.status_code, 201)

    def test_simulate_ecg_error(self):
        """Test Simulate ECG with error"""
        res = self.client.post('api/v1/signals/simulate/ecg',
                               data=json.dumps({}), content_type='application/json')
        error = json.loads(res.data)
        self.assertEqual(error, {"error": [
                         "generate_ecg() missing 10 required positional arguments: 'fs', 'noise_magnitude', 'duration', 'period', 'delay', 'P', 'Q', 'R', ""'S', and 'T'"]})
        self.assertEqual(res.status_code, 400)

    def tearDown(self):
        """
        Tear Down
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
