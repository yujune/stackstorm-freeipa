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
    <head>

    <style>


    div.container {
        background-color: #d5ebcc;
        margin-right: 5%;
        margin-left: 5%;
        margin-top: 2%;
        margin-bottom: 2%;
        border-radius: 8px;
        text-align: center;
    }

    div.body_container{
    
        background-color: #cae6f3;
        margin-right: 5%;
        margin-left: 5%;
        margin-top: 2%;
        margin-bottom: 25px;
        border-radius: 8px;
        padding-top: 1px;
        padding-bottom: 1px;
        padding-left: 20px;
        padding-right: 20px;
        font-family:Arial;
    }

    img.design{
        border-radius: 20px;
        display:block; 
        margin:auto;
    }

    a.button_design{

        text-align: center; 
        background-color: #4da64d; 
        padding:15px; 
        text-decoration: none; 
        color:white; 
        font-family:Arial; 
        border-radius: 8px;
        margin-left: 5%;
        
    }

    </style>
    
    </head>
      <body style='background:url(https://cdn.pixabay.com/photo/2017/08/10/01/49/stars-2616989_960_720.jpg); padding:2%;' >

        <div class='container' style='padding: 10px'>
            <h2 style='color: #558652; font-family:Arial;'> Self Service Password </h2> 
        </div>

        <img src="https://pbs.twimg.com/profile_images/610482584297078784/qDYij_EO_400x400.png" alt="LDAP" class='design'>

        <div class='container'  style='padding: 10px'>
            <h2 style='color: #558652; font-family:Arial;'> Change your password </h2> 
        </div>

        <div class='body_container'> 

        <h3 style='color:#357ba4'>Hi, $(receiver_name) </h3>
        <p style='color:#696969'>Your FreeIPA password is going to be expired in $(passw_daysleft) day(s).<br>
           Please click the button below to change your password.<br>
           Thank you very much!
        </p>

        </div>
        

        <a href="https://selfservice.sige.la/" class='button_design'>Change password</a>

        
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
