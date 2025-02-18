from pydantic import BaseModel, EmailStr
from datetime import datetime


class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    content: str
    send_at: datetime | None = None
