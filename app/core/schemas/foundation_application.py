import re
from pydantic import (
    BaseModel,
    validator
)
from app.core.email.email_fixer import EmailFixer


class FoundationApplication(BaseModel):
    email: str
    name: str
    project_name: str
    description: str  

    @validator("email")
    def check_email_event(cls, v):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if not re.fullmatch(regex, v):
            raise ValueError("Invalid email")
        v = EmailFixer.fix(v)
        return v