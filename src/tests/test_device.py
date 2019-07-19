import unittest
import os
import json
from src.app import create_app, db


class DeviceTest(unittest.TestCase):
    """
    Device Test Case
    """

    def setUp(self):
        """
        Test Setup
        """
        self.app = create_app("testing")
        self.client = self.app.test_client()

        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_create_device(self):
        """ Test Create Device """
        res = self.client.post('/api/v1/devices/', data=json.dumps({
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
        }), content_type='application/json')
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

    def tearDown(self):
        """
        Tear Down
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
