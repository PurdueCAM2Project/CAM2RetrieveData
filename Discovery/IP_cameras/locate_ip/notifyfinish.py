#!/usr/bin/python
import os
import sys
import smtplib
import socket
from email.mime.text import MIMEText

msg = MIMEText(socket.gethostname())
msg['Subject'] = socket.gethostname() + " finished"
msg['From'] = 'yunglu@purdue.edu'
msg['To'] = 'yunglu@purdue.edu'
sm = smtplib.SMTP('localhost')
filelist = os.listdir(".")
message = msg.as_string() + "\n\n"
for filename in filelist:
    message = message + filename + "\n"
sm.sendmail("yunglu@purdue.edu", "yunglu@purdue.edu", message)
# sm.sendmail("yunglu@purdue.edu", "yunglu@purdue.edu", msg.as_string())
sm.quit()
