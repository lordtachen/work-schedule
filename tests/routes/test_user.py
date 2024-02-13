from config import PROJECT_PATH
from utils import yaml_to_sql


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
