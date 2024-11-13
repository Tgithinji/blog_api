from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from app.jwt_handler import create_token
from app import models
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


# fixture to create new user to make login independent
@pytest.fixture
def test_user(client):
    data = {
        "username": "newuser",
        "email": "newuser@gmail.com",
        "password": "password123"
        }
    res = client.post("/users", json=data)
    new_user = res.json()
    new_user['password'] = data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_token({'user_id': test_user['id']})


@pytest.fixture
def authenticated_client(client, token):
    client.headers = {**client.headers, "Authorization": f'bearer {token}'}
    return client


@pytest.fixture
def create_posts(test_user, db):
    posts_array = [
        {
            "title": "first post",
            "content": "1st content",
            "author_id": test_user['id']
        },
        {
            "title": "second post",
            "content": "2nd content",
            "author_id": test_user['id']
        },
        {
            "title": "third post",
            "content": "3rd content",
            "author_id": test_user['id']
        }
    ]

    def create_post_model(posts):
        return models.Post(**posts)

    posts_list = list(map(create_post_model, posts_array))
    db.add_all(posts_list)
    db.commit()

    return db.query(models.Post).all()


@pytest.fixture
def create_comments(test_user, create_posts, db):
    comments_array = [
        {
            "content": "1st comment",
            "user_id" : test_user['id'],
            "post_id": create_posts[0].id
        },
        {
            "content": "1st comment",
            "user_id" : test_user['id'],
            "post_id": create_posts[0].id
        },
        {
            "content": "1st comment",
            "user_id" : test_user['id'],
            "post_id": create_posts[0].id
        }
    ]

    def create_comment_model(comments):
        return models.Comments(**comments)
    
    comments_list = list(map(create_comment_model, comments_array))

    db.add_all(comments_list)
    db.commit()

    return db.query(models.Comments).all()


@pytest.fixture
def like_post(test_user, db, create_posts):
    new_like = models.Likes(user_id=test_user['id'], post_id=create_posts[0].id)
    db.add(new_like)
    db.commit()


@pytest.fixture
def like_comment(test_user, db, create_comments):
    new_like = models.Likes(user_id=test_user['id'], comment_id=create_comments[0].id)
    db.add(new_like)
    db.commit()


@pytest.fixture
def create_users(db):
    users_array = [
        {
            "username": "user1",
            "email": "user1@gmail.com",
            "password": "password123"
        },
        {
            "username": "user2",
            "email": "user2@gmail.com",
            "password": "password123"
        }
    ]


    def create_user_model(users):
        return models.User(**users)

    users_list = list(map(create_user_model, users_array))
    db.add_all(users_list)
    db.commit()

    return db.query(models.User).all()


@pytest.fixture
def follow_user(test_user, db, create_users):
    new_follow = models.Follow(follower_id=test_user['id'], following_id=create_users[1].id)
    db.add(new_follow)
    db.commit()