import resend

from configs import settings

resend.api_key = settings.RESEND_API_KEY


def send_email(to: str, subject: str, html: str):
    try:
        response = resend.Emails.send(
            {
                "from": f"Task Manager <{settings.RESEND_FROM_EMAIL}>",
                "to": [to],
                "subject": subject,
                "html": html,
            }
        )
        return response
    except Exception as e:
        raise e
