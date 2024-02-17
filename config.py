import pathlib

CONFIG_PATH = pathlib.Path(__file__).resolve()
PROJECT_PATH = CONFIG_PATH.parent
SQLALCHEMY_DATABASE_URL = f"sqlite:///{PROJECT_PATH}/.temp/test.db"
