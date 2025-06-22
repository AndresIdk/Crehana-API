from src.infrastructure.security.password_hasher import PasswordHasher


class TestPasswordHasher:
    def test_hash_password_creates_valid_hash(self):
        password = "testpassword123"

        hashed = PasswordHasher.hash_password(password)

        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 20

    def test_hash_password_different_hashes_for_same_password(self):
        password = "testpassword123"

        hash1 = PasswordHasher.hash_password(password)
        hash2 = PasswordHasher.hash_password(password)

        assert hash1 != hash2

    def test_verify_password_correct_password(self):
        password = "testpassword123"
        hashed = PasswordHasher.hash_password(password)

        result = PasswordHasher.verify_password(password, hashed)

        assert result is True

    def test_verify_password_incorrect_password(self):
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = PasswordHasher.hash_password(password)

        result = PasswordHasher.verify_password(wrong_password, hashed)

        assert result is False

    def test_verify_password_empty_password(self):
        hashed = PasswordHasher.hash_password("testpassword")

        result = PasswordHasher.verify_password("", hashed)

        assert result is False

    def test_hash_password_special_characters(self):
        password = "test@#$%^&*()password!"

        hashed = PasswordHasher.hash_password(password)
        verified = PasswordHasher.verify_password(password, hashed)

        assert verified is True
