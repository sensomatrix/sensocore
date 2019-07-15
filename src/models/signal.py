# src/models/signal.py
from . import db
import datetime
from marshmallow import fields, Schema
from .epoch import EpochSchema, Epoch
from .data import DataSchema


class Signal(db.Model):
    """
    Signal Model
    """

    # table name
    __tablename__ = 'signal'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sensor = db.Column(db.String)
    sensor_location_on_body = db.Column(db.String)
    samples = db.Column(db.ARRAY(db.Float))
    data = db.relationship('Data', uselist=False, backref='signal')
    epochs = db.relationship('Epoch', backref='signal')
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('name')
        self.sensor = data.get('sensor')
        self.sensor_location_on_body = data.get('sensor_location_on_body')
        self.samples = data.get('samples')
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

    @staticmethod
    def get_all_signals():
        return Signal.query.all()

    @staticmethod
    def get_one_signal(id):
        return Signal.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)


class SignalSchema(Schema):
    """
    Signal Schema
    """
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    samples = fields.List(fields.Float, required=True)
    sensor = fields.String(required=True)
    sensor_location_on_body = fields.String(required=True)
    data = fields.Nested(DataSchema, many=False)
    epochs = fields.Nested(EpochSchema, many=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
