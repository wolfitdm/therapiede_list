import pickle
import os
import sys
import errno
import os.path
import smtplib
import json
import re
import time
import imaplib
import email

currentScriptDirectoryPath = os.path.dirname(os.path.abspath(__file__))
currentScriptDirectoryPathFiles = os.listdir(currentScriptDirectoryPath)

sys.path.append(currentScriptDirectoryPath)

from email.mime.text import MIMEText

def get_valid_filename(name):
    s = str(name).strip().replace(" ", "_")
    s = re.sub(r"(?u)[^-\w.]", "_", s)
    return s

def get_target(file):
    file = get_valid_filename(file)
    target_dir = "save"
    if not os.path.isdir(target_dir):
        try:
            os.makedirs(target_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
               pass
    filename = file + ".pickle"
    target = os.path.join(target_dir, filename)
    return target
    
def save_data(a, file):
    target = get_target(file)
    with open(target, 'wb') as handle:
         pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

def is_data(file):
    return os.path.isfile(get_target(file))

def load_data(file):
    target = get_target(file)
    if not os.path.isfile(target):
       return None

    with open(target, 'rb') as handle:
         b = pickle.load(handle)
         return b

def smtp_login(login, password):
    #smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    #smtpserver = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.login(login, password)
    return smtpserver
 
def smtp_server_get():
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.connect("smtp.gmail.com", 587)
    return smtpserver
   
def smtp_server_tls(smtpserver):
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
   
def email_daten_json():
    email_daten = {}
    if not os.path.isfile("email_daten.json"):
       email_daten = {
           "email": "example@gmail.com",
           "password": "app_password_created_with_2_factor_step_verification",
           "subject":  "Einzeltherapie / Gruppentherapie Transitionsbegleitung",
           "body": "Sehr geehrter Psychotherapeut/in, ich suche vorzugsweise einen Gruppentherapie Platz fuer die Transitionsbegleitung. Viele Liebe Gruesse Luna",
       }
       with open('email_daten.json', 'w') as f:
            json.dump(email_daten, f, sort_keys = False, indent = 4)
    else:
       with open("email_daten.json") as f:
            email_daten = json.load(f)
    return email_daten

email_data = email_daten_json()
login_smtp = email_data["email"]
password_smtp = email_data["password"]
email_subject = email_data["subject"]
email_body = email_data["body"]

def smtp_server_login(smtpserver):
    smtpserver.login(login_smtp, password_smtp)

def smtp_server_complete():
    smtpserver = smtp_server_get()
    smtp_server_tls(smtpserver)
    smtp_server_login(smtpserver)
    return smtpserver
    
receiver_email_cache = {}
if is_data("receiver_email_cache"):
   receiver_email_cache = load_data("receiver_email_cache")
def filter_recipients(recipients):
    res = []
    for i in range(0, len(recipients)):
        recipient = recipients[i]
        if recipient in receiver_email_cache:
           continue
        res.append(recipient)
    return res
def save_filtered_recipients(res):
    for i in range(0, len(res)):
        recipient = res[i]
        receiver_email_cache[recipient] = True
        save_data(receiver_email_cache, "receiver_email_cache")

def send_email(smtpserver, recipients):
    recipients = filter_recipients(recipients)
    subject = email_subject
    body = email_body
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = login_smtp
    msg['To'] = ', '.join(recipients)
    message_sent = True
    try:
        smtpserver.sendmail(login_smtp, recipients, msg.as_string())
    except:
        message_sent = False
    if message_sent:
       save_filtered_recipients(recipients)
    print("Message sent!")
    
def fill_receiver_email_cache():
    # Set up the IMAP connection
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(login_smtp, password_smtp)
    mail.select('"[Gmail]/Sent Mail"')  

    # Search for all email messages in the inbox
    status, data = mail.search(None, 'ALL')

    # Iterate through each email message and print its contents
    for num in data[0].split():
        status, data = mail.fetch(num, '(RFC822)')
        email_message = email.message_from_bytes(data[0][1])
        #print('From:', email_message['From'])
        #print('To:', email_message['To'])
        #print('Subject:', email_message['Subject'])
        #print('Date:', email_message['Date'])
        #print('Body:', email_message.get_payload())
        match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', email_message['To'])
        for i in range(0, len(match)):
            email_str = match[i]
            print(email_str)
            receiver_email_cache[email_str] = True
            save_data(receiver_email_cache, "receiver_email_cache")
        print()
    
    # Close the connection
    mail.close()
    mail.logout()
    
def is_email_in_cache(mail):
    if not mail == None:
       return mail in receiver_email_cache
 
mail = None 
if len(sys.argv) > 1:
   mail = sys.argv[1]
   print(mail)
print(is_email_in_cache(mail))