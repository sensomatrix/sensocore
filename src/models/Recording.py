# src/models/RecordingModel.py
from . import db
import datetime
from marshmallow import fields, Schema


class Recording(db.Model):
    """
    Recording Model
    """

    # table name
    __tablename__ = 'recording'

    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer)
    institution = db.Column(db.String)
    date = db.Column(db.DateTime)
    exp_start_time = db.Column(db.Time)
    exp_end_time = db.Column(db.Time)
    time_description = db.Column(db.String)
    visit_number = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.participant_id = data.get('participant_id')
        self.institution = data.get('institution')
        self.date = data.get('date')
        self.exp_start_time = data.get('exp_start_time')
        self.exp_end_time = data.get('exp_end_time')
        self.time_description = data.get('time_description')
        self.visit_number = data.get('visit_number')
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

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<id {}>'.format(self.id)


class RecordingSchema(Schema):
    """
    Recording Schema
    """
    id = fields.Int(dump_only=True)
    participant_id = fields.Int(required=True)
    institution = fields.String(required=True)
    date = fields.DateTime(required=True)
    exp_start_time = fields.Time(required=True)
    exp_end_time = fields.Time(required=True)
    time_description = fields.String(required=True)
    visit_number = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
