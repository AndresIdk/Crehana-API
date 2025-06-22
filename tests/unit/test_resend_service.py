from unittest.mock import patch

import pytest

from src.infrastructure.services.resend.resend_service import send_email


class TestResendService:
    @patch("src.infrastructure.services.resend.resend_service.resend.Emails.send")
    def test_send_email_success(self, mock_send):
        mock_send.return_value = {"id": "test-id", "from": "test@example.com"}

        result = send_email("test@example.com", "Test Subject", "<h1>Test HTML</h1>")

        assert result["id"] == "test-id"
        assert result["from"] == "test@example.com"
        mock_send.assert_called_once()

    @patch("src.infrastructure.services.resend.resend_service.resend.Emails.send")
    def test_send_email_with_special_characters(self, mock_send):
        mock_send.return_value = {"id": "test-id-2"}

        result = send_email(
            "test@example.com", "Test Ñoño & Co.", "<h1>Señor José's café</h1>"
        )

        assert result["id"] == "test-id-2"
        mock_send.assert_called_once()

    @patch("src.infrastructure.services.resend.resend_service.resend.Emails.send")
    def test_send_email_large_content(self, mock_send):
        mock_send.return_value = {"id": "test-id-3"}
        large_html = "<div>" + "x" * 1000 + "</div>"

        result = send_email("test@example.com", "Large Content", large_html)

        assert result["id"] == "test-id-3"
        mock_send.assert_called_once()

    @patch("src.infrastructure.services.resend.resend_service.resend.Emails.send")
    def test_send_email_api_error(self, mock_send):
        mock_send.side_effect = Exception("API Error")

        with pytest.raises(Exception, match="API Error"):
            send_email("test@example.com", "Test Subject", "<h1>Test</h1>")

    @patch("src.infrastructure.services.resend.resend_service.resend.Emails.send")
    def test_send_email_connection_error(self, mock_send):
        mock_send.side_effect = ConnectionError("Network error")

        with pytest.raises(ConnectionError, match="Network error"):
            send_email("test@example.com", "Test Subject", "<h1>Test</h1>")
