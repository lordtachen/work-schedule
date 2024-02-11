import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from app.db.session import get_db, Base
from main import app



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
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    try:
        session = TestingSessionLocal()
        
        yield session
    
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)



@pytest.fixture(scope="function")
def app_client(db_session):
    try:
        client = TestClient(app)
        app.dependency_overrides[get_db] = lambda: db_session
        yield client
    finally:
        app.dependency_overrides.clear()