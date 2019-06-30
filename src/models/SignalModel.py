# src/models/SignalModel.py
from . import db
import datetime
from marshmallow import fields, Schema


class SignalModel(db.Model):
  """
  Signal Model
  """

  # table name
  __tablename__ = 'signals'

  id = db.Column(db.Integer, primary_key=True)
  data = db.Column(db.JSON, nullable=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)
  owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.name = data.get('name')
    self.data = data.get('data')
    self.owner_id = data.get('owner_id')
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
    return SignalModel.query.all()

  @staticmethod
  def get_one_signal(id):
    return SignalModel.query.get(id)
  
  def __repr__(self):
    return '<id {}>'.format(self.id)

class SignalSchema(Schema):
  """
  User Schema
  """
  id = fields.Int(dump_only=True)
  data = fields.Str(dump_only=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)