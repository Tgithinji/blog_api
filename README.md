# Blog API

This is a blogging platform api that allows users to interact with posts.
The project is built using FastAPI and includes user authentication, post/comments creation, fetch endpoints.

[Watch live demo](https://drive.google.com/file/d/12VvO0RlefoGpfJCYZ7VPLRMhpx2c1kTI/view?usp=sharing)

## Installation

### Requirements

- Python3
- PostgreSQL

#### Steps

1. Clone the repository

```bash
git clone git@github.com:Tgithinji/blog_api.git
cd blog_api
```

2. Create and start a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependencies

```bash
pip install -r requirements.txt
```

4. Create a .env file and setup environment variables requires to connect to your database in the following order
   - SECRET_KEY: string
   - ALGORITHM: string
   - TOKEN_EXPIRY: int
   - DB_USERNAME: str
   - DB_PASSWORD: str
   - DB_HOSTNAME: str
   - DB_PORT: str
   - DB_NAME: str

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

You can test endpoints with `curl` in the terminal after the application has started successfully

Or visit `http://127.0.0.1:8000/docs` on your browser to view the api documentation by swagger UI

Or you can use postman like demonstrated in the demo video

#### Authentication

- **Login `Post`** `/login`
  Example:

```bash
curl -X POST "http://127.0.0.1:8000/login" \
-H "Content-Type: application/json" \
-d '{"username": "newuser", "password": "securepassword"}'
```

Response Body:

```json
{
  "access_token": "your-jwt-token",
  "token_type": "bearer"
}
```

#### User

- **Create User** **`Post`** `/users`
  - Authentication required
    Example

```bash
curl -X POST "http://127.0.0.1:8000/login" \
-H "Content-Type: application/json" \
-d '{
      "username": "newuser", "email": "newuser@gmail.com" "password": "securepassword"
    }'
```

Response body:

```json
{
  "username": "user1",
  "email": "user1@example.com",
  "id": "1",
  "created_at": "time created"
}
```

- **Get User `GET`** `/users/{id}`
  Example

```bash
curl -X GET http://127.0.0.1:8000/users/1
```

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

Example

```bash
curl -X GET http://127.0.0.1:8000/posts
```

- Returns all posts with their comments count
- Pagination is supported
- search query is supported to search by title

- **Get Single Post: `GET`** `/posts/{id}`
  Response body:
  Example

```bash
curl -X GET http://127.0.0.1:8000/posts/1
```

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
    "comments": 5
  }
}
```

- **Create Post: `POST`** `/posts`
  - Requires Authentication
    Response body same as getting a single post
    Example usage:

```bash
curl -X POST http://127.0.0.1:8000/posts \
     -H "Authorization: Bearer <TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"title": "My Post", "content": "This is my first post"}'
```

- **Update Post `Put`** `/posts/{id}`
- Requires authentication
  Request body same as Create Post
  Example usage:

```bash
curl -X PUT http://127.0.0.1:8000/posts/1 \
     -H "Authorization: Bearer <TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"title": "Changed Post", "content": "This is my changed post"}'
```

- **Delete Post: `Delete`** `/post{id}`
  - Deletes a post by id

```bash
curl -X GET http://127.0.0.1:8000/posts/1
```

#### Comments

- **Get comments for a single post: `GET`** `/posts/{id}/comments`
  Example

```bash
curl -X GET http://127.0.0.1:8000/posts/1/comments
```

Returns a list of comments each with the following Response body:

```json
{
  "id": 101,
  "content": "This post was really helpful!",
  "user_id": 42,
  "post_id": 1
}
```

- **Create Comment: `POST`** `posts/{id}/comments`
  - Requires Authentication
    Response body same as above

```bash
curl -X POST http://127.0.0.1:8000/posts/1/comments \
     -H "Authorization: Bearer <TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"content": "comment"}'
```

- **Delete Comment: `Delete`** `/post{id}/comments/{id}`
  - Deletes a comment by id

```bash
curl -X DELETE http://127.0.0.1:8000/posts/1comments/1
```
