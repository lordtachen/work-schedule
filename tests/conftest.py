import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from shared.config import PROJECT_PATH
from utils import yaml_to_sql
from work_schedule_backend.db.core import Base, get_db
from work_schedule_backend.main import app

# Setup the in-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# db session fixture
@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)
    try:
        session = TestingSessionLocal()

        yield session

    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def app_client(db_session):
    try:
        client = TestClient(app)
        app.dependency_overrides[get_db] = lambda: db_session
        yield client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture()
def populated_db_session(db_session):
    yaml_to_sql.load_data_from_yaml(db_session, PROJECT_PATH / "tests/mock_data")
    return db_session
