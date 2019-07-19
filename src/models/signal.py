# src/models/signal.py
from . import db
import datetime
from .epoch import EpochSchema, Epoch
from .data import DataSchema
from marshmallow import Schema, fields, validates_schema, ValidationError


class Signal(db.Model):
    """
    Signal Model
    """

    # table name
    __tablename__ = 'signal'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sensor = db.Column(db.String, nullable=True)
    sensor_location_on_body = db.Column(db.String, nullable=True)
    raw = db.Column(db.ARRAY(db.Float))
    filtered = db.Column(db.ARRAY(db.Float), nullable=True)
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
        self.raw = data.get('raw')
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
    raw = fields.List(fields.Float, required=True)
    filtered = fields.List(fields.Float)
    sensor = fields.String()
    sensor_location_on_body = fields.String()
    data = fields.Nested(DataSchema, many=False)
    epochs = fields.Nested(EpochSchema, many=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)

    @validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        validate_data = original_data if data == {} else data
        unknown = set(validate_data) - set(self.fields)
        if unknown:
            raise ValidationError('Unknown field', unknown)