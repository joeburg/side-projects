import codecs
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------#
class email:

    def __init__(self,user,password,email_file,message,messagetype,emailtype):

        # data attributes of email object
        self.user = user
        self.pwd = password
        self.message = message
        self.messagetype = messagetype
        self.recipients = None

        # load the recipients
        self.recipients = self.load_emails(email_file, emailtype)

        # message types in include: pt, html, html+pt, html+pt+alt

        # 



    def send_email_text(self, user, pwd, recipient, subject, body):

        gmail_user = user
        gmail_pwd = pwd
        FROM = user
        TO = recipient if type(recipient) is list else [recipient]
        SUBJECT = subject
        TEXT = body

        # Prepare actual message
        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
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

    def message_plaintext():


    def message_html():


    def message_html_plaintext():


    def message_html_plaintext_alt():


    def load_emails(self, recipients_file, emailtype):
        ''' imports the emails from a file and configures based on email type'''

        recipients = []
        f = open(recipients_file, 'r')
        for line in f:
            email = line.strip().split()[0]
            recipients.append(email)

        if emailtype == 'all':
            # attach all recipients on same email
            recipients = ', '.join(recipients)
            return recipients

        elif emailtype == 'individual':
            # send emails separately
            return recipients

        else:
            # raise exception
            raise Exception("Invalid email type. Must be 'all' or 'individual'")

#----------------------------------------------------------------------------------------#
# ''' simple text email '''

# user = 'joe@stonsh.com'
# pwd = 'yesjoecan2015'
# recipients = ['joeburg09@yahoo.com','rahimen@gmail.com','gislebirkeland@gmail.com']

# subject = 'craigslist reply'
# body = 'Hi!'

# # send individual emails
# Nsent = 1
# Nfail = 1
# for recipient in recipients:
#     sent = send_email_text(user,pwd,recipient,subject,body)
#     if sent:
#         print 'Number sent emails: %d' %Nsent
#         Nsent += 1
#     else:
#         print 'Number failed emails: %d ' %Nfail
#         Nfail += 1
#----------------------------------------------------------------------------------------#
''' html and plain text email '''

user = 'joe@stonsh.com'
pwd = 'yesjoecan2015'

text = '''Hi!

We are a Stanford team who built a tool that screens your CL replies, so you don't have to read through tons of emails anymore.

Watch our demo video here: http://www.stonsh.com/#video

Check it out and let us know what you think!   

Best, 

Joe Burg
Co-Founder Stonsh'''

html = '''\
<html>
  <head></head>
  <body>
    <p>Hi!</p>
    <p>We are a Stanford team who built a tool that screens your CL replies, so you don't have to read through tons of emails anymore.</p>
    <p>Watch our demo video <a href="http://www.stonsh.com/#Video">here</a>.</p>
    <p>Check it out and let us know what you think!</p>
    <p>Best,<br><br>Joe Burg<br>Co-Founder Stonsh</p>
  </body>
</html>
'''
# html = '<a href="http://www.stonsh.com/#video">Watch our demo video here!</a> </html>'

# import the emails
filename = 'test.txt'
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
    msgRoot['Subject'] = "craigslist reply"
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


# # Define these once; use them twice!
# strFrom = 'from@example.com'
# strTo = 'to@example.com'

# # Create the root message and fill in the from, to, and subject headers
# msgRoot = MIMEMultipart('related')
# msgRoot['Subject'] = 'test message'
# msgRoot['From'] = strFrom
# msgRoot['To'] = strTo
# msgRoot.preamble = 'This is a multi-part message in MIME format.'

# # Encapsulate the plain and HTML versions of the message body in an
# # 'alternative' part, so message agents can decide which they want to display.
# msgAlternative = MIMEMultipart('alternative')
# msgRoot.attach(msgAlternative)

# msgText = MIMEText('This is the alternative plain text message.')
# msgAlternative.attach(msgText)

# # We reference the image in the IMG SRC attribute by the ID we give it below
# msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
# msgAlternative.attach(msgText)

# # This example assumes the image is in the current directory
# fp = open('test.jpg', 'rb')
# msgImage = MIMEImage(fp.read())
# fp.close()

# # Define the image's ID as referenced above
# msgImage.add_header('Content-ID', '<image1>')
# msgRoot.attach(msgImage)

# # Send the email (this example assumes SMTP authentication is required)
# import smtplib
# smtp = smtplib.SMTP()
# smtp.connect('smtp.example.com')
# smtp.login('exampleuser', 'examplepass')
# smtp.sendmail(strFrom, strTo, msgRoot.as_string())
# smtp.quit()


#----------------------------------------------------------------------------------------#
# ''' html email '''

# user = 'joe@stonsh.com'
# pwd = 'yesjoecan2015'

# # when using MIME you have to use string of recipients instead of list
# recipients = ['joeburg09@gmail.com','joeburg09@yahoo.com']
# COMMASPACE = ', '
# recipients = COMMASPACE.join(recipients)

# # recipient = 'gislebirkeland@gmail.com'

# # Create message container - the correct MIME type is multipart/alternative.
# msg = MIMEMultipart('alternative')
# msg['Subject'] = "Link"
# msg['From'] = user
# msg['To'] = recipients

# # Create the body of the message (a plain-text and an HTML version).
# text = "Hi!\nHow are you?\nPlease rate the video:\n"

# # load the html document
# f = codecs.open("survey.html", 'r')
# html = f.read()
# f.close()

# # Record the MIME types of both parts - text/plain and text/html.
# part1 = MIMEText(text, 'plain')
# part2 = MIMEText(html, 'html')

# # Attach parts into message container.
# # According to RFC 2046, the last part of a multipart message, in this case
# # the HTML message, is best and preferred.
# msg.attach(part1)
# msg.attach(part2)

# send_email_html(user,pwd,recipients,msg.as_string())

