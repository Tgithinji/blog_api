from app import schemas


def test_create_comments(authenticated_client, test_user, create_posts):
    data = {
        "content": "Great comment",
        "user_id": test_user['id']
    }
    res = authenticated_client.post(
        f"/posts/{create_posts[0].id}/comments",
        json=data
    )
    new_comment = schemas.CommentsResponse(**res.json())
    assert res.status_code == 201
    assert new_comment.content == data["content"]
    assert new_comment.user_id == test_user['id']


def test_unauthorized_create_comments(client, test_user, create_posts):
    data = {
        "content": "Great comment",
        "user_id": test_user['id']
    }
    res = client.post(
        f"/posts/{create_posts[0].id}/comments",
        json=data
    )
    assert res.status_code == 401


def test_comment_nonexisting_post(authenticated_client, test_user):
    data = {
        "content": "Great comment",
        "user_id": test_user['id']
    }
    res = authenticated_client.post(
        f"/posts/99999999999999/comments",
        json=data
    )
    assert res.status_code == 404


def test_get_comments_by_post(client, create_comments, create_posts):
    res = client.get(f"/posts/{create_posts[0].id}/comments")
    assert res.status_code == 200
    assert len(create_comments) == len(res.json())


def test_get_comments_by_nonexisting_post(client):
    res = client.get(f"/posts/000000000000/comments")
    assert res.status_code == 404


def test_delete_comment(authenticated_client, create_comments, create_posts):
    res = authenticated_client.delete(f"posts/{create_posts[0].id}/comments/{create_comments[0].id}")
    assert res.status_code == 204

def test_delete_non_existing_comment(authenticated_client, create_posts):
    res = authenticated_client.delete(f"/posts/{create_posts[0].id}/comments/0000000")
    assert res.status_code == 404


def test_delete_comment_unauthorized_user(client, create_posts, create_comments):
    res = client.delete(f"/posts/{create_posts[0].id}/comments/{create_comments[0].id}")
    assert res.status_code == 401