from work_schedule_backend.data_structures.user import UserResponse
from work_schedule_backend.db import user as db_user


def test_get_user_by_id_exists(populated_db_session):
    user: UserResponse | None = db_user.get_by_id(populated_db_session, 1)

    assert user.id == 1
    assert user.name == "John Doe"
    assert isinstance(user, UserResponse)


def test_get_user_by_id_dont_exist(populated_db_session):
    user: UserResponse | None = db_user.get_by_id(populated_db_session, 100)
    assert user is None
