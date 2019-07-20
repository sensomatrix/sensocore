# src/models/epoch.py
from . import db
import datetime
from marshmallow import fields
from src.shared.custom_schema import CustomSchema


class Epoch(db.Model):
    """
    Epoch Model
    """

    # table name
    __tablename__ = 'epoch'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    duration = db.Column(db.Float)
    signal_id = db.Column(db.Integer, db.ForeignKey('signal.id'))
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('name')
        self.start_time = data.get('start_time')
        self.end_time = data.get('end_time')
        self.duration = data.get('duration')
        self.signal_id = data.get('signal_id')
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

    @staticmethod
    def get_one_epoch(id):
        return Epoch.query.get(id)

class EpochSchema(CustomSchema):
    """
    Epoch Schema
    """
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    signal_id = fields.Int(dump_only=True)
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)
    duration = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
