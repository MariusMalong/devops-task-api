def test_task_lifecycle(client):
    # Setup Auth
    client.post("/auth/register", json={"email": "dev@deakin.edu.au", "password": "Pass1234!"})
    token = client.post("/auth/login", data={"username": "dev@deakin.edu.au", "password": "Pass1234!"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create Task
    create_res = client.post("/tasks/", json={"title": "Jenkins HD", "priority": "high"}, headers=headers)
    assert create_res.status_code == 201
    task_id = create_res.json()["id"]

    # 2. Get All Tasks
    get_res = client.get("/tasks/", headers=headers)
    assert len(get_res.json()) == 1

    # 3. Filter Tasks by Priority
    filter_res = client.get("/tasks/?priority=high", headers=headers)
    assert filter_res.json()[0]["title"] == "Jenkins HD"

    # 4. Update Task (Mark Completed)
    update_res = client.put(f"/tasks/{task_id}", json={"completed": True}, headers=headers)
    assert update_res.json()["completed"] is True

    # 5. Unauthorized Access Attempt
    no_auth_res = client.delete(f"/tasks/{task_id}")
    assert no_auth_res.status_code == 401

    # 6. Delete Task
    assert client.delete(f"/tasks/{task_id}", headers=headers).status_code == 204

    # 7. Verify Deletion
    assert client.delete(f"/tasks/{task_id}", headers=headers).status_code == 404