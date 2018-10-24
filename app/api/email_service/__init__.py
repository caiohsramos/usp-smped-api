from dotenv import load_dotenv, find_dotenv
import os
import smtplib

load_dotenv(find_dotenv())

class Email:
    def __init__(self):
        self.email = os.environ.get('GMAIL_EMAIL', '')
        self.password = os.environ.get('GMAIL_PASSWORD', '')
        self.server = smtplib.SMTP('smtp.gmail.com:587')
        self.server.ehlo()
        self.server.starttls()
        self.server.login(self.email, self.password)
    
    def send_email(self, emails, subject, message):
        #usa self.server para mandar email
        email_text = f"""\
From: {self.email}  
To: {", ".join(emails)}  
Subject: {subject}

{message}"""

        self.server.sendmail(self.email, emails, email_text)

    def close_server(self):
        self.server.close()
        