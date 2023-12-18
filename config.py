import os
import pathlib

CONFIG_PATH = pathlib.Path(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URL = f"sqlite:///{CONFIG_PATH.parent}/test.db"
