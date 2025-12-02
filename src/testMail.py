
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------- CONFIG ----------
sender_email = "mohammedhasnaine2005@gmail.com"
receiver_email = "mohammedmultazam17@gmail.com"
password = "eczm ngaf icei wllh"  # Use an App Password, not your Gmail password
subject = "Test Email from Python"
body = "Hello, this is a test email sent from Python!"

# ---------- CREATE MESSAGE ----------
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = subject

msg.attach(MIMEText(body, "plain"))

# ---------- SEND EMAIL ----------
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Secure connection
        server.login(sender_email, password)
        server.send_message(msg)
        print("Email sent successfully!")
except Exception as e:
    print("Error:", e)
