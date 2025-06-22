from fastapi import status


class TestTaskEndpoints:
    def test_get_all_tasks_success(self, client, test_task, auth_headers):
        response = client.get("/tasks/", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status_code"] == 200
        assert "Tasks retrieved successfully" in data["message"]
        assert isinstance(data["data"], list)

    def test_create_task_success(self, client, test_list_task, auth_headers):
        task_data = {
            "title": "New Task",
            "description": "New Task Description",
            "status": "Pending",
            "priority": "High",
            "completeness": "0%",
            "id_list_task": test_list_task.id_list_task,
        }

        response = client.post("/tasks/", json=task_data, headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status_code"] == 201
        assert "Task created successfully" in data["message"]
        task_response = data["data"]
        assert task_response["title"] == task_data["title"]
        assert task_response["description"] == task_data["description"]

    def test_create_task_invalid_data(self, client, auth_headers):
        task_data = {
            "title": "",
            "description": "Test Description",
            "status": "InvalidStatus",
            "priority": "InvalidPriority",
            "completeness": "InvalidCompleteness",
            "id_list_task": 999,
        }

        response = client.post("/tasks/", json=task_data, headers=auth_headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_task_by_id_success(self, client, test_task, auth_headers):
        response = client.get(f"/tasks/{test_task.id_task}", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status_code"] == 200
        assert "Task retrieved successfully" in data["message"]
        task_response = data["data"]
        assert task_response["id_task"] == test_task.id_task

    def test_get_task_by_id_not_found(self, client, auth_headers):
        response = client.get("/tasks/999", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status_code"] == 500

    def test_update_task_success(self, client, test_task, auth_headers):
        update_data = {
            "title": "Updated Task Title",
            "description": "Updated Task Description",
        }

        response = client.put(
            f"/tasks/{test_task.id_task}", json=update_data, headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status_code"] == 200
        assert "Task updated successfully" in data["message"]

    def test_update_task_not_found(self, client, auth_headers):
        update_data = {"title": "Updated Task Title"}

        response = client.put("/tasks/999", json=update_data, headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status_code"] == 500

    def test_delete_task_success(self, client, test_task, auth_headers):
        response = client.delete(f"/tasks/{test_task.id_task}", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status_code"] == 200
        assert "Task deleted successfully" in data["message"]

    def test_delete_task_not_found(self, client, auth_headers):
        response = client.delete("/tasks/999", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status_code"] == 500

    def test_get_tasks_by_list_task_id(
        self, client, test_task, test_list_task, auth_headers
    ):
        response = client.get(
            f"/tasks/list/{test_list_task.id_list_task}", headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status_code"] == 200
        assert "Tasks retrieved successfully" in data["message"]
        assert isinstance(data["data"], list)

    def test_update_task_status_success(self, client, test_task, auth_headers):
        status_data = {"status": "Completed"}

        response = client.put(
            f"/tasks/{test_task.id_task}/status", json=status_data, headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status_code"] == 200
        assert "Task status updated successfully" in data["message"]

    def test_create_task_missing_required_fields(self, client, auth_headers):
        task_data = {"title": "Test Task"}

        response = client.post("/tasks/", json=task_data, headers=auth_headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_task_crud_flow(self, client, test_list_task, db_session, auth_headers):
        create_data = {
            "title": "CRUD Test Task",
            "description": "CRUD Test Description",
            "status": "Pending",
            "priority": "Medium",
            "completeness": "0%",
            "id_list_task": test_list_task.id_list_task,
        }

        create_response = client.post("/tasks/", json=create_data, headers=auth_headers)
        assert create_response.status_code == status.HTTP_200_OK
        created_task = create_response.json()["data"]
        task_id = created_task["id_task"]

        read_response = client.get(f"/tasks/{task_id}", headers=auth_headers)
        assert read_response.status_code == status.HTTP_200_OK
        task_data = read_response.json()["data"]
        assert task_data["title"] == create_data["title"]

        update_data = {
            "title": "Updated CRUD Task",
            "description": "Updated CRUD Description",
        }
        update_response = client.put(
            f"/tasks/{task_id}", json=update_data, headers=auth_headers
        )
        assert update_response.status_code == status.HTTP_200_OK

        delete_response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
        assert delete_response.status_code == status.HTTP_200_OK
