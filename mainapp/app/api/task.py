from fastapi import APIRouter, HTTPException
from schemas.email import EmailRequest
from tasks.email_tasks import send_email


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/send-email", response_model=dict, summary="Send email")
def send_email_task(email_data: EmailRequest):
    eta_time = email_data.send_at if email_data.send_at else None
    task = send_email.apply_async(
        args=[
            email_data.to,
            email_data.subject,
            email_data.content,
        ],
        eta=eta_time,
    )
    # send email
    return {
        "task_id": task.id,
        "status": "Scheduled" if email_data.send_at else "Preccesing Started",
        "scheduled_at": email_data.send_at.isoformat() if email_data.send_at else None,
    }
