from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
import pytest


DATABASE_URL = f'postgresql+psycopg2://postgres:password@localhost:5432/test_blog_api'
engine = create_engine(DATABASE_URL)
Testing_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db():
    # drop all tables before test
    Base.metadata.drop_all(bind=engine)

    Base.metadata.create_all(bind=engine)
    session = Testing_SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
