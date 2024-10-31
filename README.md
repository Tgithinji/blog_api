# Blog API

This is a blogging platform api that allows users to interact with posts.
The project is built using FastAPI and includes user authentication, post/comments creation, fetch endpoints.

## Installation

### Requirements

- Python 3.9+
- PostgreSQL

#### Steps

1. Clone the repository

```bash
git@github.com:Tgithinji/blog_api.git
cd blog_api
```

2. Create and start a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependancies

```bash
pip install -r requirements.txt
```

4. Create a .env file and setup environment variables requires to connect to your database in the following order
   - secret_key: string
   - algorithm: string
   - access_token_expire_minutes: int
   - database_username: str
   - database_password: str
   - database_hostname: str
   - database_port: str
   - database_name: str

#### Usage

1. The API uses Alembic for migrations so run the following

```bash
alembic revision --autogenerate -m "Migration message"
alembic upgrade head
```

2. Start the application

```bash
fastapi dev app/main.py
```

## EndPoints

#### Authentication

- **Login `Post`** `/login`
  Example:
  Request body:

```json
{
  "username": "user@example.com",
  "password": "yourpassword"
}
```

Response Body:

```json
{
  "access_token": "your-jwt-token",
  "token_type": "bearer"
}
```

#### User

- **Create User** **`Post`** `/users` - Authentication required
  Request body:

```json
{
  "username": "user1",
  "email": "user1@example.com",
  "password": "yourpassword"
}
```

- **Get User `GET`** `/users/{id}`
  Response body:

```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john_doe@example.com"
  },
  "post": 3
}
```

#### Posts

- **Get All Posts: `GET`** `/posts`

  - Returns all posts with their comments count
  - Pagination is supported
  - search query is supported to search by title

- **Get Single Post: `GET`** `/posts/{id}`
  Response body:

```json
{
  "post": {
    "id": 1,
    "title": "Understanding FastAPI Relationships",
    "content": "This post explains how to use FastAPI to manage relationships...",
    "created_at": "2024-10-15T10:00:00Z",
    "author": {
      "username": "jane_doe",
      "email": "jane_doe@example.com"
    },
    "comment_count": 5
  }
}
```

- **Create Post: `POST`** `/posts` - Requires Authentication
  Request body:

```json
{
  "title": "Post Title",
  "content": "Post content"
}
```

- **Update Post `Put`** `/posts/{id}`
  - Requires authentication
    Request body same as Create Post
- **Delete Post: `Delete`** `/post{id}`
  - Deletes a post by id

#### Comments

- **Get Single comment: `GET`** `/posts/{id}/comments{id}`
  Response body:

```json
{
  "id": 101,
  "content": "This post was really helpful!",
  "user_id": 42,
  "post_id": 1
}
```

- **Create Comment: `POST`** `/comments` - Requires Authentication
  Request body:

```json
{
  "content": "comment"
}
```

- **Delete Comment: `Delete`** `/post{id}/comments/{id}`
  - Deletes a comment by id

## Example usage

You can test endpoints with `curl` in the terminal after the application has started successfully

- Fetch all posts

```bash
curl -X GET http://127.0.0.1:8000/posts
```

- Create a post

```bash
curl -X POST http://127.0.0.1:8000/posts \
     -H "Authorization: Bearer <TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"title": "My Post", "content": "This is my first post"}'
```

- Login a user

```bash
curl -X POST "http://127.0.0.1:8000/login" \
-H "Content-Type: application/json" \
-d '{"username": "newuser", "password": "securepassword"}'
```
