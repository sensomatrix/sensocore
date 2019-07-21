import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from src.models.signal import Signal
from src.models.data import Data
from src.models.device import Device
from src.models.epoch import Epoch

from src.app import create_app, db

env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)

migrate = Migrate(app=app, db=db, signal=Signal,
                  data=Data, device=Device, epoch=Epoch)

manager = Manager(app=app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
