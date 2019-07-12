import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from src.models.User import User
from src.models.Signal import Signal
from src.models.Data import Data
from src.models.Device import Device
from src.models.Epoch import Epoch
from src.models.Recording import Recording

from src.app import create_app, db

env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)

migrate = Migrate(app=app, db=db, user=User, signal=Signal,
                  data=Data, device=Device, epoch=Epoch, recording=Recording)

manager = Manager(app=app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
