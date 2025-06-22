from fastapi import status


class TestAuthEndpoints:
    def test_register_user_success(self, client):
        user_data = {"email": "newuser@example.com", "password": "password123"}

        response = client.post("/auth/register", json=user_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "newuser@example.com" in data["message"]
        assert "registered successfully" in data["message"]

    def test_register_user_duplicate_email(self, client, test_user):
        user_data = {"email": test_user.email, "password": "password123"}

        response = client.post("/auth/register", json=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "detail" in data

    def test_register_user_invalid_email(self, client):
        user_data = {"email": "invalid-email", "password": "password123"}

        response = client.post("/auth/register", json=user_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_user_short_password(self, client):
        user_data = {"email": "test@example.com", "password": "123"}

        response = client.post("/auth/register", json=user_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_user_missing_fields(self, client):
        user_data = {"email": "test@example.com"}

        response = client.post("/auth/register", json=user_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_login_user_success(self, client, test_user):
        login_data = {"email": test_user.email, "password": "testpassword123"}

        response = client.post("/auth/login", json=login_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "token" in data
        assert "logged in successfully" in data["message"]
        assert len(data["token"]) > 0

    def test_login_user_invalid_email(self, client):
        login_data = {"email": "nonexistent@example.com", "password": "password123"}

        response = client.post("/auth/login", json=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert "detail" in data

    def test_login_user_invalid_password(self, client, test_user):
        login_data = {"email": test_user.email, "password": "wrongpassword"}

        response = client.post("/auth/login", json=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert "detail" in data

    def test_register_and_login_flow(self, client):
        user_data = {"email": "flowtest@example.com", "password": "password123"}

        register_response = client.post("/auth/register", json=user_data)
        assert register_response.status_code == status.HTTP_200_OK

        login_response = client.post("/auth/login", json=user_data)
        assert login_response.status_code == status.HTTP_200_OK

        login_data = login_response.json()
        assert "token" in login_data
        assert len(login_data["token"]) > 0
