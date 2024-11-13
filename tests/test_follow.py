def test_follow_user(authenticated_client, create_users):
    res = authenticated_client.post(
        f"/users/{create_users[1].id}/follow",
    )
    assert res.status_code == 201


def test_follow_user_unauthenticated(client, create_users):
    res = client.post(
        f"/users/{create_users[1].id}/follow",
    )
    assert res.status_code == 401


def test_follow_non_existing_user(authenticated_client, create_users):
    res = authenticated_client.post(
        f"/users/999999999999999999999999999999999999/follow",
    )
    assert res.status_code == 404


def test_follow_themselves(authenticated_client, create_users):
    res = authenticated_client.post(
        f"/users/{create_users[0].id}/follow",
    )
    assert res.status_code == 400


def test_unfollow_user(authenticated_client, create_users, follow_user):
    res = authenticated_client.delete(
        f"/users/{create_users[1].id}/unfollow",
    )
    assert res.status_code == 204


def test_unfollow_user_unauthenticated(client, create_users):
    res = client.delete(
        f"/users/{create_users[1].id}/unfollow",
    )
    print(res.json())
    assert res.status_code == 401


def test_unfollow_non_existing_user(authenticated_client, create_users):
    res = authenticated_client.delete(
        f"/users/999999999999999999999999999999999999/unfollow",
    )
    assert res.status_code == 404
    