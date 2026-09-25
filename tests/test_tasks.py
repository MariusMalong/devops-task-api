def test_task_lifecycle(client):
    # Register and login
    client.post("/auth/register", json={"email": "dev@deakin.edu.au", "password": "Pass1234!"})
    login_res = client.post("/auth/login", data={"username": "dev@deakin.edu.au", "password": "Pass1234!"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create task
    create_res = client.post(
        "/tasks/",
        json={"title": "Implement Jenkins Pipeline", "description": "High Distinction Task", "priority": "high"},
        headers=headers,
    )
    assert create_res.status_code == 201
    task_id = create_res.json()["id"]

    # Read tasks
    get_res = client.get("/tasks/", headers=headers)
    assert get_res.status_code == 200
    assert len(get_res.json()) == 1

    # Update task
    update_res = client.put(f"/tasks/{task_id}", json={"completed": True}, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["completed"] is True

    # Delete task
    del_res = client.delete(f"/tasks/{task_id}", headers=headers)
    assert del_res.status_code == 204