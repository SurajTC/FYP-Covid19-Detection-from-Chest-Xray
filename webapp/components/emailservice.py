import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# mail_content = '''Hello,
# This is a simple mail. There is only text, no attachments are there The mail is sent using Python SMTP library.
# Thank You
# '''

# #The mail addresses and password
# sender_address = 'batch05.cse.mit@gmail.com'
# sender_pass = 'batch05csemit'
# receiver_address = 'surzavn@gmail.com'
# #Setup the MIME
# message = MIMEMultipart()
# message['From'] = sender_address
# message['To'] = receiver_address
# message['Subject'] = 'A test mail sent by Python. It has an attachment.'   #The subject line
# #The body and the attachments for the mail
# message.attach(MIMEText(mail_content, 'plain'))
# #Create SMTP session for sending the mail
# session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
# session.starttls() #enable security
# session.login(sender_address, sender_pass) #login with mail_id and password
# text = message.as_string()
# session.sendmail(sender_address, receiver_address, text)
# session.quit()
# print('Mail Sent') 

file = open(r'static/data/gmail_key','r').readlines()
sender = {'email': file[0].rstrip(), 'password': file[1].rstrip()}

def recover_password(user):
  content = f'''
  This is an auto-genrated email ,
  below you can find the details of your account

  Username : {user['username']}
  Password : {user['password']}

  Thank You
  '''

  message = MIMEMultipart()
  message['From']= sender['email']
  message['To'] = user['email']
  message['Subject'] = 'Password Recovery for Batch-05 Project'
  message.attach(MIMEText(content, 'plain'))

  try:
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender['email'], sender['password'])
    response = message.as_string()
    session.sendmail(sender['email'], user['email'], response)
    print("Email sent: password recovery")
  except:
   print("Error: unable to send email")


def send_verification(object):
  content = f'''
  This is an auto-genrated email ,
  below you can find the verification code

  Username          : {object['username']}
  Verification Code : {object['code']}

  Thank You
  '''
  message = MIMEMultipart()
  message['From']= sender['email']
  message['To'] = object['email']
  message['Subject'] = 'Verification Code for Batch-05 Project'
  message.attach(MIMEText(content, 'plain'))

  try:
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender['email'], sender['password'])
    response = message.as_string()
    session.sendmail(sender['email'], object['email'], response)
    print("Email sent: verification")
  except:
   print("Error: unable to send email")


def send_result(object):
  content = f'''
  This is an auto-genrated email ,
  below you can find the Predicted Result

  Chance of being Covid-19 Positive : {object['covid']}
  Chance of being Covid-19 Negative : {object['normal']}
  Prediction : {object['result']}

  Thank You
  '''
  message = MIMEMultipart()
  message['From']= sender['email']
  message['To'] = object['email']
  message['Subject'] = 'Predicted Result (Batch-05 Project)'
  message.attach(MIMEText(content, 'plain'))

  try:
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender['email'], sender['password'])
    response = message.as_string()
    session.sendmail(sender['email'], object['email'], response)
    print("Email sent: Prediction")
  except:
   print("Error: unable to send email")