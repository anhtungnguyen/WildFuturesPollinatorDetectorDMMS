import cv2
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send email notification
def send_email_notification():
    # Email configuration
    sender_email = "tungnguyen68mufc@gmail.com"
    receiver_email = "anhtungnguyen1809@gmail.com"
    password = "ichk ydiq alcv govd "  # Use App Password if 2FA is enabled

    # Email content
    subject = "Raspberry Pi Notification - Video Recording Completed"
    body = "DONE"

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email notification sent successfully.")
    except Exception as e:
        print(f"Failed to send email notification: {e}")


# Send email notification
send_email_notification()
