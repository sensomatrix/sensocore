# src/models/device.py
from . import db
import datetime
from marshmallow import fields, Schema
from .signal import Signal, SignalSchema


class Device(db.Model):
    """
    Device Model
    """

    # table name
    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    type = db.Column(db.String)
    company = db.Column(db.String)
    sin = db.Column(db.Integer)
    channel_num = db.Column(db.Integer)
    signals = db.relationship('Signal', backref='device')
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('name')
        self.type = data.get('type')
        self.company = data.get('company')
        self.sin = data.get('sin')
        self.channel_num = data.get('channel_num')
        self.time_description = data.get('time_description')
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


class DeviceSchema(Schema):
    """
    Device Schema
    """
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    type = fields.String(required=True)
    company = fields.String(required=True)
    sin = fields.Int(required=True)
    channel_num = fields.Int(required=True)
    signals = fields.Nested(SignalSchema, many=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
