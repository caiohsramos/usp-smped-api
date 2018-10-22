from dotenv import load_dotenv, find_dotenv
import os
import smtplib

load_dotenv(find_dotenv())

class Email:
    def __init__(self):
        self.email = os.environ.get('GMAIL_EMAIL', '')
        self.password = os.environ.get('GMAIL_PASSWORD', '')
        self.server = smtplib.SMTP('smtp.gmail.com:587').ehlo().starttls()
        self.server.login(self.email, self.password)
    
    def send_email(self, email, message):
        #usa self.server para mandar email
        pass
        