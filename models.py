from app import db
from sqlalchemy.dialects.postgresql import JSON


class Signal(db.Model):
    __tablename__ = 'signals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    unit = db.Column(db.String())
    fs = db.Column(db.Integer())

    def __init__(self, name, unit, fs):
        self.name = name
        self.unit = unit
        self.fs = fs

    def __repr__(self):
        return '<id {}>'.format(self.id)