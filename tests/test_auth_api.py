from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "email": "api-test1@test.com",
            "password": "MonMotDePasse123!",
        }
    )
    
    assert response.status_code == 201
    
    data = response.json()
    
    assert data["email"] == "api-test1@test.com"
    assert data["is_active"] is True
    assert "id" in data
    assert "password_hash" not in data

def test_register_duplicate_email():
    response = client.post(
        "/auth/register",
        json={
            "email": "api-test1@test.com",
            "password": "MonMotDePasse123!",
        },
    )

    assert response.status_code == 409

    data = response.json()

    assert data["detail"] == (
        "An existing user with this email is already exists"
    )
    
def test_register_invalid_email():
    response = client.post(
        "/auth/register",
        json={
            "email": "ceci-n-est-pas-un-email",
            "password": "MonMotDePasse123!",
        },
    )

    assert response.status_code == 422

def test_register_short_password():
    response = client.post(
        "/auth/register",
        json={
            "email": "short@test.com",
            "password": "123",
        },
    )

    assert response.status_code == 422