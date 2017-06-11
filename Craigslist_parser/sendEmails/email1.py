import codecs
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#----------------------------------------------------------------------------------------#
def send_email_html(user,pwd,recipient,message):
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        return True
    except:
        return False

def send_ssl_email_html(user,pwd,recipient,message):
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]

    try:
        # SMTP_SSL
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo() # optional, called by login()
        server_ssl.login(gmail_user, gmail_pwd)  
        # ssl server doesn't support or need tls, so don't call server_ssl.starttls() 
        server_ssl.sendmail(FROM, TO, message)
        server_ssl.close()
        return True
    except:
        return False
#----------------------------------------------------------------------------------------#
''' html and plain text email '''

user = 'joe@stonsh.com'
pwd = 'yesjoecan2015'

text = '''Hi!

We are a Stanford team who built a tool for Property Managers that automatically screens tenants based on their Craigslist replies, so you don't have to read through tons of emails and waste time on weak leads anymore.

Watch our demo video here: http://www.stonsh.com/#Video

Check it out and let us know what you think!   

Best, 

Joe Burg
Co-Founder Stonsh'''

html = '''\
<html>
  <head></head>
  <body>
    <p>Hi!</p>
    <p>We are a Stanford team who built a tool for Property Managers that automatically screens tenants based on their Craigslist replies, so you don't have to read through tons of emails and waste time on weak leads anymore.</p>
    <p>Watch our demo video <a href="http://www.stonsh.com/#Video">here</a>.</p>
    <p>Check it out and let us know what you think!</p>
    <p>Best,<br><br>Joe Burg<br>Co-Founder Stonsh</p>
  </body>
</html>
'''

#----------------------------------------------------------------------------------------#
# import the emails
filename = 'clean_CL_emails2.txt'
recipients = []
f = open(filename, 'r')
for line in f:
    email = line.strip().split()[0]
    recipients.append(email)

# send individual emails
Nsent = 1
Nfail = 1
for recipient in recipients:
    # make the message
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = "Re: craigslist reply"
    msgRoot['From'] = user
    msgRoot['To'] = recipient
    msgRoot.preamble = 'This is a multi-part message.'

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msgAlternative.attach(part1)
    msgAlternative.attach(part2)

    # send the message
    sent = send_ssl_email_html(user,pwd,recipient,msgRoot.as_string())
    if sent:
        print 'Number sent emails: %d' %Nsent
        Nsent += 1
    else:
        print 'Number failed emails: %d ' %Nfail
        Nfail += 1

