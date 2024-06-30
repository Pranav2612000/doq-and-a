from dotenv import load_dotenv
import smtplib
import ssl
import os

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
PORT = 587
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("GOOGLE_PASSWORD")

print(EMAIL, PASSWORD)

context = ssl.create_default_context()

def send_email(receiver_email, message):
    with smtplib.SMTP(SMTP_SERVER, PORT) as server:
        server.connect('smtp.gmail.com', '587')
        server.ehlo()
        server.starttls(context=context)  # Secure the connection
        server.ehlo()
        server.login(EMAIL, PASSWORD)

        server.sendmail(EMAIL, receiver_email, message)
