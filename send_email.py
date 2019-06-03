#!/usr/bin/env python

import smtplib
import subprocess

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "tanakhate@gmail.com"
receiver_email = "tanakhate@gmail.com"
cmd = raw_input("Command to execute --> ")
password = raw_input("Type your password and press enter: ")
result = subprocess.check_output(cmd,shell=True)
print("Sending:-\n"+result)
try:
    server = smtplib.SMTP(smtp_server,port)
    server.starttls() # Secure the connection
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, result)
except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit() 

# import smtplib

# server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
# server.login("tanakhate@gmail.com", "cr74ever")
# server.sendmail(
#   "tanakhate@gmail.com", 
#   "tanakhate@gmail.com", 
#   "this message is from python")
# server.quit()