#src/models/__init__.py
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

# initialize our db
db = SQLAlchemy()
bcrypt = Bcrypt()