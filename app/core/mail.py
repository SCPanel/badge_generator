import ssl
import smtplib
from os import getenv
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

async def send_message(email, subject, content):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = getenv("contact_email")
    message["To"] = email

    part2 = MIMEText(content, "html")

    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(message["From"], getenv("contact_email_password"))
        server.sendmail(
            message["From"], message["To"], message.as_string()
        )