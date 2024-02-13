import pathlib
from typing import Any, Sequence

import yaml
from sqlalchemy.orm import Session

from work_schedule_backend.db.models import *  # noqa: F401, F403


def load_data(session: Session, data: Sequence[dict[str, Any]]):
    for entry in data:
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
