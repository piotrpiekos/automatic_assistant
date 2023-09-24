from src.actions import ActionClass

import smtplib
from email.mime.text import MIMEText


class SendEmail(ActionClass):
    def __init__(self, username: str):
        super(SendEmail, self).__init__(username)

        self.sender = self.profile['email']['address']
        self.email_pwd = self.profile['email']['password']

    def log(self, recipient, subject, text):
        self.logtext('Sending email from: ', self.sender, ' to ', recipient,'. Subject: ', subject)

    def execute(self, recipient: str, subject: str, text: str):
        msg = MIMEText(text)

        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = recipient

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(self.sender, self.email_pwd)
            smtp_server.sendmail(self.sender, recipient, msg.as_string())
