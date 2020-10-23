import sys
from st2common.runners.base_action import Action
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SendEmail(Action):

  def run(self, receiver_name, receiver_email, passw_daysleft):
    
    account = self.config.get('smtp_account', None)

    if account is None:
      raise ValueError('"smtp_accounts" config value is required to send email.') 
    
    sender_email = account['username']
    password = account['password']
    
    msg = MIMEMultipart()
    msg['Subject'] = "Password Expiration Warning"
    msg['From'] = sender_email
    msg['To'] = receiver_email  

    subject = "Password Expiration Warning"

    body = "Hi, " + receiver_name + ".\n" + "Your freeipa password is going to be expired in " + str(passw_daysleft) + " day(s)."
    #server = smtplib.SMTP('smtp.gmail.com', 587)   # connect to SMTP server (Google mail server address )
    server = smtplib.SMTP( account['server'], account['port'])

    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()

    #message = 'Subject: {subject}\n\n{body}'

    server.starttls()    # encrypt the traffic
    server.login(sender_email, password)    # login 
    print("Login Success")

    server.sendmail(sender_email, receiver_email, text)
    print("The email has been sent to " + receiver_email)
    server.quit()

    return(True)
