"""REST API Tests: CRUD endpoints and negative response validation."""
import pytest
from utils.api_client import APIClient

@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.regression
def test_get_posts_list(api: APIClient):
    """
    Scenario: Verify GET /posts returns a list of resources.
    Expectation: HTTP 200, JSON array containing expected attributes.
    """
    response = api.get("/posts")
    assert response.status_code == 200
    assert response.headers.get("Content-Type", "").startswith("application/json")

    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) > 0

    first_post = posts[0]
    for key in ["userId", "id", "title", "body"]:
        assert key in first_post

@pytest.mark.api
@pytest.mark.regression
def test_get_single_post_by_id(api: APIClient):
    """
    Scenario: Verify GET /posts/{id} retrieves specific entity.
    Expectation: HTTP 200, resource ID matches request.
    """
    post_id = 1
    response = api.get(f"/posts/{post_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == post_id
    assert len(data["title"]) > 0

@pytest.mark.api
@pytest.mark.regression
def test_get_non_existent_post_returns_404(api: APIClient):
    """
    Negative Scenario: Request non-existent entity.
    Expectation: HTTP 404 Not Found.
    """
    response = api.get("/posts/9999999")
    assert response.status_code == 404

@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.regression
def test_create_new_post(api: APIClient):
    """
    Scenario: Verify POST /posts creates a new resource.
    Expectation: HTTP 201 Created, response reflects payload and assigns ID.
    """
    payload = {
        "title": "Automated Test Post",
        "body": "Created via Playwright & Requests automated framework.",
        "userId": 1,
    }
    response = api.post("/posts", json=payload)
    assert response.status_code == 201

    created = response.json()
    assert created["title"] == payload["title"]
    assert created["body"] == payload["body"]
    assert created["userId"] == payload["userId"]
    assert "id" in created

@pytest.mark.api
@pytest.mark.regression
def test_update_existing_post(api: APIClient):
    """
    Scenario: Verify PUT /posts/{id} updates existing resource.
    Expectation: HTTP 200 OK, payload values updated.
    """
    post_id = 1
    update_payload = {
        "id": post_id,
        "title": "Updated Title via Regression Suite",
        "body": "Updated content.",
        "userId": 1,
    }
    response = api.put(f"/posts/{post_id}", json=update_payload)
    assert response.status_code == 200

    updated = response.json()
    assert updated["title"] == update_payload["title"]

@pytest.mark.api
@pytest.mark.regression
def test_delete_post(api: APIClient):
    """
    Scenario: Verify DELETE /posts/{id} deletes resource.
    Expectation: HTTP 200 OK.
    """
    response = api.delete("/posts/1")
    assert response.status_code in [200, 204]
