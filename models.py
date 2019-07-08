from app import db, bcrypt
from sqlalchemy.dialects.postgresql import JSON
from marshmallow import fields, Schema

class Signal(db.Model):
    __tablename__ = 'signals'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForgeignKey('users.id'), nullable=False)
    data = db.Column(db.Text())

    def __init__(self, data):
        self.data = data
        self.owner_id = data.get('owner_id')

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


class SignalSchema(Schema):
  """
  Signal Schema
  """
  id = fields.Int(dump_only=True)
  data = fields.String(dump_only=True)



class UserModel(db.Model):
    """
    User Model
    """

    # table name
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    signals = db.relationship('Signal', backref='signals', lazy=True)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('name')
        self.email = data.get('email')
        self.password = self.__generate_has(data.get('password'))
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password': # add this new line
                self.password = self.__generate_hash(value) # add this new line
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_one_user(id):
        return UserModel.query.get(id)

  
    def __repr__(self):
        return '<id {}>'.format(self.id)


class UserSchema(Schema):
    """
    User Schema
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    signals = fields.Nested(SignalSchema, many=True)
