# src/models/data.py
from . import db
import datetime
from marshmallow import fields, Schema


class Data(db.Model):
    """
    Data Model
    """

    # table name
    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    channel_num = db.Column(db.Integer)
    description = db.Column(db.Text)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    duration = db.Column(db.Float)
    fs = db.Column(db.Integer)
    unit = db.Column(db.String)
    signal_id = db.Column(db.Integer, db.ForeignKey(
        'signal.id'), nullable=False)
    signal = db.relationship('Signal', back_populates="data")
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.channel_num = data.get('channel_num')
        self.description = data.get('description')
        self.start_time = data.get('start_time')
        self.end_time = data.get('end_time')
        self.duration = data.get('duration')
        self.fs = data.get('fs')
        self.unit = data.get('unit')
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


class DataSchema(Schema):
    """
    Data Schema
    """
    id = fields.Int(dump_only=True)
    channel_num = fields.Int(required=True)
    description = fields.String(required=True)
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)
    duration = fields.Int(required=True)
    fs = fields.Int(required=True)
    unit = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
