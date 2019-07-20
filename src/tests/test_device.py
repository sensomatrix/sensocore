import unittest
import os
import json
from src.app import create_app, db
from marshmallow import ValidationError
from src.models.device import Device, DeviceSchema

class DeviceModelTest(unittest.TestCase):
    """
    Device Model Test Case
    """

    def setUp(self):
        """
        Test Setup
        """
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.device_schema = DeviceSchema()
        self.test_data = {
            "name": "Niro's Device",
            "type": "ECG",
            "company": "SmartHalo",
            "sin": 123445,
            "channel_num": 1,
            "signals": [
                {
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
            ]
        }

        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_display_device_none(self):
        """ Test Display device using repr"""
        device_data, _ = self.device_schema.load(self.test_data)

        device = Device(device_data)
        self.assertEqual(repr(device), '<id None>')

    def tearDown(self):
        """
        Tear Down
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

class DeviceViewTest(unittest.TestCase):
    """
    Device View Test Case
    """

    def setUp(self):
        """
        Test Setup
        """
        self.test_data = {
            "name": "Niro's Device",
            "type": "ECG",
            "company": "SmartHalo",
            "sin": 123445,
            "channel_num": 1,
            "signals": [
                {
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
            ]
        }
        self.app = create_app("testing")
        self.client = self.app.test_client()

        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_create_device(self):
        """ Test Create Device """
        res = self.client.post(
            '/api/v1/devices/', data=json.dumps(self.test_data), content_type='application/json')
        self.assertEqual(res.status_code, 201)

    def test_create_device_error(self):
        """ Test Create Device Error"""
        res = self.client.post(
            '/api/v1/devices/', data=json.dumps({}), content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(data, {'channel_num': ['Missing data for required field.'],
                                'company': ['Missing data for required field.'],
                                'name': ['Missing data for required field.'],
                                'sin': ['Missing data for required field.'],
                                'type': ['Missing data for required field.']})
        self.assertEqual(res.status_code, 400)

    def test_get_devices(self):
        """ Test Get Devices """
        res = self.client.post(
            '/api/v1/devices/', data=json.dumps(self.test_data), content_type='application/json')
        self.assertEqual(res.status_code, 201)

        res = self.client.get('/api/v1/devices/',
                              content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(res.status_code, 200)

    def test_get_device(self):
        """Test Get One Device"""
        res = self.client.post(
            '/api/v1/devices/', data=json.dumps(self.test_data), content_type='application/json')
        self.assertEqual(res.status_code, 201)

        res = self.client.get('/api/v1/devices/1',
                              content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_get_device_error(self):
        """Test Attempt to get one device that does not exist"""
        res = self.client.get('/api/v1/devices/1',
                              content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_update_device_nonexistant(self):
        """Test Update a device that does not exist"""
        res = self.client.put('/api/v1/devices/3', data=json.dumps({}),
                              content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_update_device(self):
        """Test Update an existing device"""
        res = self.client.post(
            '/api/v1/devices/', data=json.dumps(self.test_data), content_type='application/json')
        self.assertEqual(res.status_code, 201)

        new_name = 'Updated ECG Device'
        res = self.client.put('/api/v1/devices/1', data=json.dumps({"name": new_name}),
                              content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(data['name'], new_name)
        self.assertEqual(res.status_code, 200)

    def test_update_device_load_error(self):
        """Test Attempt to update an existing device"""
        res = self.client.post(
            '/api/v1/devices/', data=json.dumps(self.test_data), content_type='application/json')
        self.assertEqual(res.status_code, 201)

        res = self.client.put('/api/v1/devices/1', data=json.dumps({"inavlid": "invalid"}),
                              content_type='application/json')
        self.assertRaises(ValidationError)
        self.assertEqual(res.status_code, 400)

    def test_delete_device(self):
        """Test Delete a device"""
        res = self.client.post(
            '/api/v1/devices/', data=json.dumps(self.test_data), content_type='application/json')
        self.assertEqual(res.status_code, 201)

        res = self.client.delete(
            '/api/v1/devices/1', content_type='application/json')
        self.assertEqual(res.status_code, 204)

    def test_delete_device_nonexistant(self):
        """Test Delete a device non existant"""
        res = self.client.delete(
            '/api/v1/devices/1', content_type='application/json')
        self.assertEqual(res.status_code, 404)
        self.assertEqual({'error': 'device not found'}, json.loads(res.data))

    def tearDown(self):
        """
        Tear Down
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
