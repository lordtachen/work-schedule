import yaml
import pathlib
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, Base, engine
from app.models.user import User, Permission


def load_data(session: Session, data: list):
    for entry in data:
        model_class = globals()[entry["model"]]
        model_data = entry["data"]

        for item_data in model_data:
            item = model_class(**item_data)
            session.add(item)


if __name__ == "__main__":
    yaml_file_path = "/home/ctw00914/external/work-schedule/tests/data"  # Update with the path to your YAML file

    # Create tables in the database
    Base.metadata.create_all(bind=engine)
    try:
        session = SessionLocal()
        for f in pathlib.Path(yaml_file_path).glob("**/*.yaml"):
            load_data(session, yaml.safe_load(f.read_text()))
        session.commit()
    except Exception as ex:
        print(ex)
        session.rollback()
    finally:
        session.close()
