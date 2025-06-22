from fastapi import status


class TestListTaskEndpoints:
    def test_get_all_list_tasks_success(self, client, test_list_task, auth_headers):
        response = client.get("/list_tasks/", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status_code"] == 200
        assert "List tasks retrieved successfully" in data["message"]
        assert isinstance(data["data"], list)

    def test_create_list_task_success(self, client, auth_headers):
        list_task_data = {
            "title": "New List Task",
            "description": "New List Task Description",
        }

        response = client.post(
            "/list_tasks/", json=list_task_data, headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status_code"] == 200
        assert "List task created successfully" in data["message"]
        list_task_response = data["data"]
        assert list_task_response["title"] == list_task_data["title"]
        assert list_task_response["description"] == list_task_data["description"]

    def test_create_list_task_missing_required_fields(self, client, auth_headers):
        list_task_data = {"title": "Test List Task"}

        response = client.post(
            "/list_tasks/", json=list_task_data, headers=auth_headers
        )

        assert response.status_code in [
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        ]

    def test_update_list_task_success(self, client, test_list_task, auth_headers):
        update_data = {
            "title": "Updated List Task Name",
            "description": "Updated List Task Description",
        }

        response = client.put(
            f"/list_tasks/{test_list_task.id_list_task}",
            json=update_data,
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status_code"] == 200
        assert "List task updated successfully" in data["message"]
        list_task_response = data["data"]
        assert list_task_response["title"] == update_data["title"]
        assert list_task_response["description"] == update_data["description"]

    def test_delete_list_task_success(self, client, test_list_task, auth_headers):
        response = client.delete(
            f"/list_tasks/{test_list_task.id_list_task}", headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status_code"] == 200
        assert "List task deleted successfully" in data["message"]
        assert data["data"] is None

    def test_list_task_crud_flow(self, client, db_session, auth_headers):
        create_data = {
            "title": "CRUD Test List Task",
            "description": "CRUD Test Description",
        }

        create_response = client.post(
            "/list_tasks/", json=create_data, headers=auth_headers
        )
        assert create_response.status_code == status.HTTP_200_OK
        created_list_task = create_response.json()["data"]
        list_task_id = created_list_task["id_list_task"]

        read_response = client.get("/list_tasks/", headers=auth_headers)
        assert read_response.status_code == status.HTTP_200_OK
        list_tasks = read_response.json()["data"]
        found_task = next(
            (lt for lt in list_tasks if lt["id_list_task"] == list_task_id), None
        )
        assert found_task is not None
        assert found_task["title"] == create_data["title"]

        update_data = {
            "title": "Updated CRUD List Task",
            "description": "Updated CRUD Description",
        }
        update_response = client.put(
            f"/list_tasks/{list_task_id}", json=update_data, headers=auth_headers
        )
        assert update_response.status_code == status.HTTP_200_OK
        updated_list_task = update_response.json()["data"]
        assert updated_list_task["title"] == update_data["title"]

        delete_response = client.delete(
            f"/list_tasks/{list_task_id}", headers=auth_headers
        )
        assert delete_response.status_code == status.HTTP_200_OK
        assert delete_response.json()["data"] is None

    def test_create_multiple_list_tasks_same_user(self, client, auth_headers):
        list_task_data_1 = {
            "title": "First List Task",
            "description": "First Description",
        }
        list_task_data_2 = {
            "title": "Second List Task",
            "description": "Second Description",
        }

        response_1 = client.post(
            "/list_tasks/", json=list_task_data_1, headers=auth_headers
        )
        response_2 = client.post(
            "/list_tasks/", json=list_task_data_2, headers=auth_headers
        )

        assert response_1.status_code == status.HTTP_200_OK
        assert response_2.status_code == status.HTTP_200_OK

        list_task_1 = response_1.json()["data"]
        list_task_2 = response_2.json()["data"]

        assert list_task_1["title"] == list_task_data_1["title"]
        assert list_task_2["title"] == list_task_data_2["title"]
        assert list_task_1["id_list_task"] != list_task_2["id_list_task"]
