from core.celery import celery_app
import time


@celery_app.task(name="tasks.email_tasks.send_email")
def send_email(to: str, subject: str, content: str):
    print(f"Email sent to {to} with subject {subject}")
    time.sleep(5)
    print(f"Sent email to {to}")
    return {
        "status": "sent",
        "email": to,
        "subject": subject,
    }
