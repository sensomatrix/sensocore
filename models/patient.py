
class Patient:
    """object that holds patient info"""

    def __init__(self, patient_id=None, age=None, address=None, bday=None, sex=None, instituition=None, date=None,
                 visit_num=None, device_name=None, channels=None):
        self.patient_id = patient_id
        self.age = age
        self.address = address
        self.bday = bday
        self.sex = sex
        self.instituition = instituition
        self.date = date
        self.visit_num = visit_num
        self.device_name = device_name
        self.channels = channels