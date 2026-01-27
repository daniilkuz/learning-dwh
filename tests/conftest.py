import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.config.database import Base, get_db, SQLALCHEMY_DATABASE_URL

# For async testing with httpx
from httpx import AsyncClient

from seed_database import create_sample_data
import os

# # SQLite database URL for testing
# SQLITE_DATABASE_URL = "sqlite:///./test_db.db"

DB_HOST = os.getenv("DB_TEST_HOST", "localhost")
DB_PORT = os.getenv("DB_TEST_PORT", "54321")
DB_NAME = os.getenv("DB_TEST_NAME", "fastapi_db")
DB_USER = os.getenv("DB_TEST_USER", "postgres")
DB_PASSWORD = os.getenv("DB_TEST_PASSWORD", "postgres")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    with TestingSessionLocal() as session:
        create_sample_data(session)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="session")
def db_session(db_engine):
    # connection = db_engine.connect()
    # transaction = connection.begin()
    # session = TestingSessionLocal(bind=connection)
    # yield session
    # session.close()
    # transaction.rollback()
    # connection.close()
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="session")
def client(db_session):
    # Override get_db dependency
    def override_get_db():
        try:
            yield db_session
        finally:
            # print("override_get_db finished")
            pass
            # db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

# # Async client fixture
# @pytest.fixture
# async def async_client():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         yield ac