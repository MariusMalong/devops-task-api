def test_register_and_login(client):
    # Register user
    reg_response = client.post(
        "/auth/register",
        json={"email": "test@deakin.edu.au", "password": "SecurePassword123!"},
    )
    assert reg_response.status_code == 201
    assert reg_response.json()["email"] == "test@deakin.edu.au"

    # Login user
    login_response = client.post(
        "/auth/login",
        data={"username": "test@deakin.edu.au", "password": "SecurePassword123!"},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()