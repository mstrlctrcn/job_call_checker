import os
from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib
#load_dotenv() searches for a .env in the current directory and loads its values.
def send_message(message_text):
	msg = EmailMessage()
	load_dotenv()
	sending_email = os.getenv("MY_GMAIL_USERNAME")
	receiving_email = os.getenv("MY_RECEIVING_EMAIL")
	secret_code = os.getenv("MY_SECRET_KEY")
	msg["Subject"] = "Job Calls"
	msg.set_content(message_text)
	msg["From"] = sending_email
	msg["To"] = receiving_email
	# Open a secure connection pipe
	try:
		with smtplib.SMTP("smtp.gmail.com", 587) as server:
		    server.starttls()  # Secure the connection
		    server.login(sending_email, secret_code)
		    server.send_message(msg)
	except Exception as e:
		print(f"an error occurred: {e}")
