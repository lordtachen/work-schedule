import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from tests.helpers import yaml_to_sql
from app.db.session import get_db, Base
from main import app
from config import PROJECT_PATH

client = TestClient(app)

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


# Dependency to override the get_db dependency in the main app
def override_get_db():
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()


app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def populated_db():
    Base.metadata.create_all(bind=engine)

    try:
        session = TestingSessionLocal()
        yaml_to_sql.load_data_from_yaml(session, PROJECT_PATH / "tests/data")
        yield session
    finally:
        session.close()

    Base.metadata.drop_all(bind=engine)



def test_delete_user(populated_db):
    response = client.delete("users/1")
    assert response.status_code == 200, response.text


def test_user_get(populated_db):
    response = client.get("users/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "John Doe"
