from config import PROJECT_PATH
from utils import yaml_to_sql

# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine, StaticPool
# from sqlalchemy.orm import sessionmaker
# from work_schedule_backend.db.session import get_db, Base
# from main import app
# from config import SQLALCHEMY_DATABASE_URL


# # Setup the in-memory SQLite database for testing
# #DATABASE_URL = "sqlite:///:memory:"
# DATABASE_URL = SQLALCHEMY_DATABASE_URL
# engine = create_engine(
#     DATABASE_URL,
#     connect_args={
#         "check_same_thread": False,
#     },
#     poolclass=StaticPool,
# )

# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# # db session fixture
# @pytest.fixture(scope="function")
# def db_session():
#     Base.metadata.create_all(bind=engine)
#     try:
#         session = TestingSessionLocal()

#         yield session

#     finally:
#         session.close()
#         Base.metadata.drop_all(bind=engine)

# app_client = TestClient(app)
# app.dependency_overrides[get_db] = lambda: TestingSessionLocal()


def test_delete_user(db_session, app_client):
    yaml_to_sql.load_data_from_yaml(db_session, PROJECT_PATH / "tests/mock_data")
    response = app_client.delete("users/1")
    assert response.status_code == 200, response.text


def test_user_get(db_session, app_client):
    yaml_to_sql.load_data_from_yaml(db_session, PROJECT_PATH / "tests/mock_data")
    response = app_client.get("users/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "John Doe"
