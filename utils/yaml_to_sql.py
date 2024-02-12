import pathlib

import yaml
from sqlalchemy.orm import Session

from work_schedule_backend.models.permission import Permission
from work_schedule_backend.models.user import User


def load_data(session: Session, data: list):
    for entry in data:
        print(data)
        model_class = globals()[entry["model"]]
        model_data = entry["data"]

        for item_data in model_data:
            item = model_class(**item_data)
            session.add(item)


def load_data_from_yaml(session: Session, data_dir: pathlib.Path):
    try:
        for f in pathlib.Path(data_dir).glob("**/*.yaml"):
            load_data(session, yaml.safe_load(f.read_text()))
        session.commit()
    except Exception as ex:
        print(ex)
        session.rollback()
    finally:
        session.close()
