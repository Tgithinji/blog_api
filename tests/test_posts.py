from app import models, schemas


def test_get_posts(client, create_posts):
    res = client.get("/posts")
    assert res.status_code == 200
    assert len(create_posts) == len(res.json())


def test_get_one_post(client, create_posts):
    res = client.get(f"/posts/{create_posts[0].id}")
    assert res.status_code == 200
    post = schemas.PostWithComments(**res.json())
    assert post.Post.id == create_posts[0].id


def test_post_not_found(client):
    res = client.get(f"/posts/77777777")
    assert res.status_code == 404


def test_create_post(authenticated_client, test_user):
    data = {
            "title": "sample post",
            "content": "sample content",
            "author_id": test_user['id']
        }
    res = authenticated_client.post("/posts", json=data)
    new_post = schemas.PostReturned(**res.json())
    assert res.status_code == 201
    assert new_post.title == data['title']


def test_create_post_unauthorized_user(client, test_user):
    data = {
            "title": "sample post",
            "content": "sample content",
            "author_id": test_user['id']
        }
    res = client.post("/posts", json=data)
    assert res.status_code == 401


def test_update_post(authenticated_client, create_posts):
    data = {
            "title": "changed post",
            "content": "changed content"
        }
    res = authenticated_client.put(f"/posts/{create_posts[0].id}", json=data)
    assert res.status_code == 200
    new_post = schemas.PostReturned(**res.json())
    assert new_post.title == data['title']
    assert new_post.content == data['content']


def test_unauthorized_update_post(client, create_posts):
    data = {
            "title": "changed post",
            "content": "changed content"
        }
    res = client.put(f"/posts/{create_posts[0].id}", json=data)
    assert res.status_code == 401


def test_update_non_existing_post(authenticated_client, create_posts):
    data = {
            "title": "changed post",
            "content": "changed content"
        }
    res = authenticated_client.put(f"/posts/888888", json=data)
    assert res.status_code == 404


def test_delete_post(authenticated_client, create_posts):
    res = authenticated_client.delete(f"/posts/{create_posts[0].id}")
    assert res.status_code == 204


def test_delete_non_existing_post(authenticated_client, create_posts):
    res = authenticated_client.delete(f"/posts/0000000")
    assert res.status_code == 404