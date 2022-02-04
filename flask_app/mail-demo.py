import smtplib
import os
from email.message import EmailMessage 

USER_NAME = os.environ.get('DB_USER')
PASSWORD = os.environ.get('DB_PASS')
print(PASSWORD)

msg = EmailMessage()
msg['subject'] = "Grab dinner this weekend?"
msg['From'] = USER_NAME
msg['To'] = 'szhou089@gmail.com'
msg.set_content('How about dinner at 6pm this Saturday?') 

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(USER_NAME , PASSWORD)

    smtp.send_message(msg)