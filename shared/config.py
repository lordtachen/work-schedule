import pathlib

CONFIG_PATH = pathlib.Path(__file__).resolve()
PROJECT_PATH = CONFIG_PATH.parent.parent
pathlib.Path(PROJECT_PATH / ".temp").mkdir(parents=True, exist_ok=True)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{PROJECT_PATH}/.temp/test.db"
