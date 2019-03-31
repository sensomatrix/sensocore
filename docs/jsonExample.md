```json
{
	"JSONFILE_Raw_Template": {
		"header": {
			"group1": [
				{
					"type": "raw",
					"index": 3
				},
				{
					"type": "processed",
					"index": 8
				},
				{
					"type": "raw",
					"index": 11
				}
			],
			"accelorometers": [
				{
					"type": "raw",
					"index": 5
				},
				{
					"type": "raw",
					"index": 6
				},
				{
					"type": "raw",
					"index": 7
				}
			],
			"patient_information": {
				"id": "",
				"age": "_NaN_",
				"weight": "_NaN_",
				"height": "_NaN_",
				"address": "",
				"birthdate": "",
				"full_name": "",
				"sex": ""
			},
			"recording_info": {
				"instituition": "",
				"address": "",
				"admin_name": "",
				"admin_id": "",
				"date": "",
				"time_description": "Eastern Time (US & Canada)",
				"visit_num": "_NaN_",
				"saved_location_on_disk_or_network": ""
			},
			"device_information": {
				"name": "",
				"type": "",
				"company": "",
				"SIN": "",
				"channel_num": 6,
				"channel1": {
					"name": "IBI",
					"sensor": "PPG",
					"sensor_location_on_body": "",
					"data": {
						"dimension": 2,
						"description": [
							"Time of the beat with respect to the start time",
							"Duration"
						],
						"start_time": [
							"11:38:00",
							"11:38:00.02"
						],
						"end_time": [
							"12:55:00.04",
							"12:55:00"
						],
						"duration": [
							"01:17:00",
							"01:17:00.14"
						],
						"fs": "_NaN_",
						"unit": [
							"Seconds",
							"Seconds"
						]
					}
				},
				"channel2": {
					"name": "BVP",
					"sensor": "PPG",
					"sensor_location_on_body": "Wrist",
					"data": {
						"dimension": 1,
						"description": "Blood Volume Pressure",
						"start_time": "11:38:00",
						"end_time": "12:55:00",
						"duration": "01:17:00",
						"fs": 64,
						"unit": "Fraction of nanoWatt (nW)"
					}
				},
				"channel3": {
					"name": "HR",
					"sensor": "PPG",
					"sensor_location_on_body": "Wrist",
					"data": {
						"dimension": 1,
						"description": "Heart Rate",
						"start_time": "11:38:00",
						"end_time": "12:55:00",
						"duration": "01:17:00",
						"fs": 1,
						"unit": "BPM"
					}
				},
				"channel4": {
					"name": "TEMP",
					"sensor": "Thermopile",
					"sensor_location_on_body": "Wrist",
					"data": {
						"dimension": 1,
						"description": "Temperature",
						"start_time": "11:38:00",
						"end_time": "12:55:00",
						"duration": "01:17:00",
						"fs": 4,
						"unit": "Celsius"
					}
				},
				"channel5": {
					"name": "ACC",
					"sensor": "Accelerometer",
					"sensor_location_on_body": "Wrist",
					"data": {
						"dimension": 3,
						"description": [
							"gravitational force applied to spacial dimensions x",
							"gravitational force (g) applied to spacial dimensions y",
							"gravitational force (g) applied to spacial dimensions z"
						],
						"start_time": [
							"11:38:00",
							"11:38:00.07",
							"11:38:00.80"
						],
						"end_time": [
							"12:55:00.19",
							"12:55:00",
							"12:55:00"
						],
						"duration": [
							"01:17:00.45",
							"01:17:00.98",
							"01:17:00.67"
						],
						"fs": [32,32,32],
						"unit": [
							"Gravitational Force (g)",
							"Gravitational Force (g)",
							"Gravitational Force (g)"
						]
					}
				},
				"channel6": {
					"name": "EDA",
					"sensor": "EDA",
					"sensor_location_on_body": "Wrist",
					"data": {
						"dimension": 1,
						"description": "Electrodermal Activity",
						"start_time": "11:38:00",
						"end_time": "12:55:00",
						"duration": "01:17:00",
						"fs": 4,
						"unit": "Microsiemens (?S)"
					}
				}
			},
			"epoch_information": {
				"channel1": {
					"epoch_num": 3,
					"epoch1": {
						"name": "Video",
						"start_time": "11:43:00",
						"end_time": "11:51:00",
						"duration": "00:08:00"
					},
					"epoch2": {
						"name": "Demo",
						"start_time": "11:58:00",
						"end_time": "12:10:00",
						"duration": "00:12:00"
					},
					"epoch3": {
						"name": "Recall",
						"start_time": "12:44:00",
						"end_time": "12:47:00",
						"duration": "00:03:00"
					}
				},
				"channel2": {
					"epoch_num": 3,
					"epoch1": {
						"name": "Video",
						"start_time": "11:43:00",
						"end_time": "11:51:00",
						"duration": "00:08:00"
					},
					"epoch2": {
						"name": "Demo",
						"start_time": "11:58:00",
						"end_time": "12:10:00",
						"duration": "00:12:00"
					},
					"epoch3": {
						"name": "Recall",
						"start_time": "12:44:00",
						"end_time": "12:47:00",
						"duration": "00:03:00"
					}
				},
				"channel3": {
					"epoch_num": 3,
					"epoch1": {
						"name": "Video",
						"start_time": "11:43:00",
						"end_time": "11:51:00",
						"duration": "00:08:00"
					},
					"epoch2": {
						"name": "Demo",
						"start_time": "11:58:00",
						"end_time": "12:10:00",
						"duration": "00:12:00"
					},
					"epoch3": {
						"name": "Recall",
						"start_time": "12:44:00",
						"end_time": "12:47:00",
						"duration": "00:03:00"
					}
				},
				"channel4": {
					"epoch_num": 3,
					"epoch1": {
						"name": "Video",
						"start_time": "11:43:00",
						"end_time": "11:51:00",
						"duration": "00:08:00"
					},
					"epoch2": {
						"name": "Demo",
						"start_time": "11:58:00",
						"end_time": "12:10:00",
						"duration": "00:12:00"
					},
					"epoch3": {
						"name": "Recall",
						"start_time": "12:44:00",
						"end_time": "12:47:00",
						"duration": "00:03:00"
					}
				},
				"channel5": {
					"epoch_num": 3,
					"epoch1": {
						"name": "Video",
						"start_time": "11:43:00",
						"end_time": "11:51:00",
						"duration": "00:08:00"
					},
					"epoch2": {
						"name": "Demo",
						"start_time": "11:58:00",
						"end_time": "12:10:00",
						"duration": "00:12:00"
					},
					"epoch3": {
						"name": "Recall",
						"start_time": "12:44:00",
						"end_time": "12:47:00",
						"duration": "00:03:00"
					}
				},
				"channel6": {
					"epoch_num": 3,
					"epoch1": {
						"name": "Video",
						"start_time": "11:43:00",
						"end_time": "11:51:00",
						"duration": "00:08:00"
					},
					"epoch2": {
						"name": "Demo",
						"start_time": "11:58:00",
						"end_time": "12:10:00",
						"duration": "00:12:00"
					},
					"epoch3": {
						"name": "Recall",
						"start_time": "12:44:00",
						"end_time": "12:47:00",
						"duration": "00:03:00"
					}
				}
			},
			"processing_information": {
				"channel1": {
					"epoch1": {
					},
					"epoch2": {
					},
					"epoch3": {
					}
				},
				"channel2": {
					"epoch1": {
					},
					"epoch2": {
					},
					"epoch3": {
					}
				},
				"channel3": {
					"epoch1": {
					},
					"epoch2": {
					},
					"epoch3": {
					}
				},
				"channel4": {
					"epoch1": {
					},
					"epoch2": {
					},
					"epoch3": {
					}
				},
				"channel5": {
					"epoch1": {
					},
					"epoch2": {
					},
					"epoch3": {
					}
				},
				"channel6": {
					"epoch1": {
					},
					"epoch2": {
					},
					"epoch3": {
					}
				}
			}
		},
		"Raw_Signal": {
			"channel1": {
				"data": null
			},
			"channel2": {
				"data": null
			},
			"channel3": {
				"data": null
			},
			"channel4": {
				"data": null
			},
			"channel5": {
				"data": null
			},
			"channel6": {
				"data": null
			}
		},
		"Processed_Signal": {
			"channel1": {
				"epoch1": {
				},
				"epoch2": {
				},
				"epoch3": {
				}
			},
			"channel2": {
				"epoch1": {
				},
				"epoch2": {
				},
				"epoch3": {
				}
			},
			"channel3": {
				"epoch1": {
				},
				"epoch2": {
				},
				"epoch3": {
				}
			},
			"channel4": {
				"epoch1": {
				},
				"epoch2": {
				},
				"epoch3": {
				}
			},
			"channel5": {
				"epoch1": {
				},
				"epoch2": {
				},
				"epoch3": {
				}
			},
			"channel6": {
				"epoch1": {
				},
				"epoch2": {
				},
				"epoch3": {
				}
			}
		}
	}
}

```