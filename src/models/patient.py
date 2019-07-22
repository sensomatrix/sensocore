# src/models/data.py
from . import db
import datetime
from marshmallow import fields
from src.shared.custom_schema import CustomSchema


class Patient(db.Model):
    """
    Patient Model
    """

    # table name
    __tablename__ = 'patient'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer)
    full_name = db.Column(db.String)
    height = db.Column(db.String)
    weight = db.Column(db.String)
    age = db.Column(db.Integer)
    address = db.Column(db.Text)
    birthdate = db.Column(db.Date)
    sex = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.patient_id = data.get('patient_id')
        self.age = data.get('age')
        self.address = data.get('address')
        self.birthdate = data.get('birthday')
        self.full_name = data.get('full_name')
        self.height = data.get('height')
        self.weight = data.get('weight')
        self.sex = data.get('sex')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()


class PatientSchema(CustomSchema):
    """
    Patient Schema
    """
    id = fields.Int(dump_only=True)
    patient_id = fields.Int(require=True)
    age = fields.Int(required=True)
    height = fields.String(required=True)
    weight = fields.String(required=True)
    full_name = fields.String(required=True)
    address = fields.String(required=True)
    birthdate = fields.Date(required=True)
    sex = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
