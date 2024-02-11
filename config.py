import os
import pathlib

CONFIG_PATH = pathlib.Path(os.path.abspath(__file__))
PROJECT_PATH = CONFIG_PATH.parent
SQLALCHEMY_DATABASE_URL = f"sqlite:///{PROJECT_PATH}/.temp/test.db"
