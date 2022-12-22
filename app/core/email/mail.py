import ssl
import smtplib
from app.core.config import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

async def send_message(email, subject, content):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = settings.CONTACT_EMAIL
    message["To"] = email

    part2 = MIMEText(content, "html")

    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(message["From"], settings.CONTACT_EMAIL_PASSWORD)
        server.sendmail(
            message["From"], message["To"], message.as_string()
        )