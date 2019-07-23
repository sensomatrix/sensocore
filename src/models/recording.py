# src/models/data.py
from . import db
import datetime
from marshmallow import fields
from src.shared.custom_schema import CustomSchema


class Recording(db.Model):
    """
    Recording Model
    """

    # table name
    __tablename__ = 'recording'

    id = db.Column(db.Integer, primary_key=True)
    instituition = db.Column(db.String)
    address = db.Column(db.String)
    date = db.Column(db.Date)
    time_description = db.Column(db.String)
    visit_num = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.instituition = data.get('institution')
        self.address = data.get('address')
        self.date = data.get('date')
        self.time_description = data.get('time_description')
        self.visit_num = data.get('visit_num')
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


class RecordingSchema(CustomSchema):
    """
    Recording Schema
    """
    id = fields.Int(dump_only=True)
    instituition = fields.String(required=True)
    address = fields.String(required=True)
    date = fields.Date(required=True)
    time_description = fields.String(required=True)
    visit_num = fields.Integer(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
