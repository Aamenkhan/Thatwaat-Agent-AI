import smtplib
from email.mime.text import MIMEText
from config import EMAIL_ADDRESS, EMAIL_PASSWORD

def send_email(to_address, subject, body):
    """Send an email using SMTP"""
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("Email credentials not configured.")
        return False

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_address

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def read_emails():
    """Placeholder for reading emails using IMAP"""
    print("Connecting to IMAP server to read emails...")
    return []
