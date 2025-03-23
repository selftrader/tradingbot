import smtplib
from email.mime.text import MIMEText
from core.config import EMAIL_HOST, EMAIL_PORT, EMAIL_USERNAME, EMAIL_PASSWORD
from twilio.rest import Client
from core.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

def send_trade_email(subject, body, recipient_email):
    """Send a trade execution alert via Email."""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USERNAME
    msg["To"] = recipient_email

    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USERNAME, recipient_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"❌ Email Alert Failed: {e}")




def send_trade_sms(message, recipient_number):
    """Send a trade execution alert via SMS."""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=recipient_number)
    except Exception as e:
        print(f"❌ SMS Alert Failed: {e}")
