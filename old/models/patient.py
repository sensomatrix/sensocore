from PyQt5.QtCore import pyqtSignal, QObject


class Patient:
    """object that holds patient info"""

    def __init__(self, patient_id=None, age=None, address=None, bday=None, sex=None, instituition=None, date=None,
                 visit_num=None, device_name=None, channels=None, patient_info=None):
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
        self.patient_info = patient_info


class PatientListModel(QObject):
    """object that holds the list of Patient objects and notifies the QTreeWidget used in the UI when changes occur"""
    patientCreated = pyqtSignal(Patient)

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.patients = []

    def append_patient(self, patient):
        self.patients.append(patient)
        self.patientCreated.emit(patient)