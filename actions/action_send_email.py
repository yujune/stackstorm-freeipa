import sys
from st2common.runners.base_action import Action
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SendEmail(Action):

    def run(self, receiver_name, receiver_email, passw_daysleft):

        account = self.config.get('smtp_account', None)

        if account is None:
            raise ValueError(
                '"smtp_accounts" config value is required to send email.')

        sender_email = account['username']
        password = account['password']

        msg = MIMEMultipart()
        msg['Subject'] = "Password Expiration Warning"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        body = "Hi, " + receiver_name + ".\n" + \
            "Your freeipa password is going to be expired in " + \
            str(passw_daysleft) + " day(s)."

        body = '<p>Hello, ' + receiver_name + '. Your freeipa password is going to be expired in ' + \
            str(passw_daysleft) + ' day(s).<br> Please <a href="www.google.com">click here</a> to change your password. Thank you very much.</p>'
        # server = smtplib.SMTP('smtp.gmail.com', 587)   # connect to SMTP server (Google mail server address )

        html = """\
    <html>
      <body>
        <h1>Hi, $(receiver_name) </h1>
        <p>Your freeipa password is going to be expired in $(passw_daysleft) day(s).<br>
           Please <a href="https://selfservice.sige.la/">click here</a> to change your password.<br>
           Thank you very much!
        </p>
      </body>
    </html>
"""
        html = html.replace("$(receiver_name)", receiver_name)
        html = html.replace("$(passw_daysleft)", str(passw_daysleft))
        server = smtplib.SMTP(account['server'], account['port'])

        msg.attach(MIMEText(html, 'html'))
        text = msg.as_string()

        server.starttls()    # encrypt the traffic
        server.login(sender_email, password)    # login
        print("Login Success")

        server.sendmail(sender_email, receiver_email, text)
        del msg

        print("The email has been sent to " + receiver_email)
        server.quit()

        return(True)
