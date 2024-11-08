def test_like_post(authenticated_client, create_posts, test_user):
    res = authenticated_client.post(
        f"/posts/{create_posts[0].id}/likes",
        json={"user_id": test_user['id']}
    )
    assert res.status_code == 201
    assert res.json()['message'] == "You liked post"


def test_unlike_post(authenticated_client, create_posts, test_user, like_post):
    res = authenticated_client.post(
        f"/posts/{create_posts[0].id}/likes",
        json={"user_id": test_user['id']}
    )
    assert res.status_code == 201
    assert res.json()['message'] == "You unliked post"


def test_like_post_unauthorized_user(client, create_posts, test_user):
    res = client.post(
        f"/posts/{create_posts[0].id}/likes",
        json={"user_id": test_user['id']}
    )
    assert res.status_code == 401


def test_like__nonexisting_post(authenticated_client, test_user):
    res = authenticated_client.post(
        f"/posts/0000000000/likes",
        json={"user_id": test_user['id']}
    )
    assert res.status_code == 404


def test_like_comment(authenticated_client, create_posts, test_user, create_comments):
    res = authenticated_client.post(
        f"/posts/{create_posts[0].id}/comments/{create_comments[0].id}/likes",
        json={"user_id": test_user['id']}
    )
    assert res.status_code == 201
    assert res.json()['message'] == "You liked comment"


def test_unlike_comment(authenticated_client, create_posts, test_user, create_comments, like_comment):
    res = authenticated_client.post(
        f"/posts/{create_posts[0].id}/comments/{create_comments[0].id}/likes",
        json={"user_id": test_user['id']}
    )
    assert res.status_code == 201
    assert res.json()['message'] == "You unliked comment"


def test_like_comment_unauthorized(client, create_posts, test_user, create_comments):
    res = client.post(
        f"/posts/{create_posts[0].id}/comments/{create_comments[0].id}/likes",
        json={"user_id": test_user['id']}
    )
    assert res.status_code == 401


def test_like_nonexisting_comment(authenticated_client, test_user, create_posts):
    res = authenticated_client.post(
        f"/posts/{create_posts[0].id}/comments/6564446664/likes",
        json={"user_id": test_user['id']}
    )
    assert res.status_code == 404

