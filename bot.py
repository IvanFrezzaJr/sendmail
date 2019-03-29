from getpass import getpass
import os
import time
import smtplib, ssl
import config
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def main():
    # Solicita o assunto. Pode ser configurado no arquivo config.py
    subject = config.EMAIL_SUBJECT
    while not subject:
        subject = input("Enter subject:")


    # Solicita a mensagem. Pode ser configurado no arquivo config.py
    body = config.EMAIL_MESSAGE
    while not body:
        body = input("Enter message:")

    # Solicita um email destinatario.
    # Pode ser configurado no arquivo config.py um arquivo.
    # Esse arquivo pode ter uma lista de e-mails.
    print('setting mail list ...')
    receiver = emailfile_to_array(config.CONTACTS_FILE)
    while not receiver:
        receiver = input("You don't have e-mail list. Enter receiver email:")
    print('mail list successfully completed!')

    # Solicita o password. Pode ser configurado no arquivo config.py
    password = config.EMAIL_PASSWORD
    while not password:
        password = getpass("Enter password:")
    
    # prepara a mensagem MIME
    print('setting the message ...')
    attachfile = config.EMAIL_ATTACHFILE 
    messageMIMEObject = create_message(subject, body, attachfile)
    print('message successfully completed!')

    # Cria o SMTP
    smtp = create_server(config.SMTP_SERVER, config.SMTP_PORT, config.EMAIL_ADDRESS, password)
    
    # Prepara a fila de e-mails
    print('-----------------------')
    print('starting sending emails')
    for email in receiver:
        message = get_string_message(messageMIMEObject, email)
        # send email
        send_email(smtp, email, message)
        time.sleep(5)
    print('-----------------------')
    print('Emails sent successfully!')
    close_server(smtp)
    
    
# pega os e-mails do arquivo e coloca em um array.
def emailfile_to_array(contactsfile):
    content = []
    with open(contactsfile,  "r", encoding="utf-8-sig") as f:
        [ content.append(l.strip('\n')) for l in f.readlines() if l != '' ]
    return content


# prepara mensagem MIME
def create_message(subject, body, attachfile):    
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = config.EMAIL_ADDRESS
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    if attachfile:
        # Open PDF file in binary mode
        with open(attachfile, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {attachfile}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)

    return message



def get_string_message(messageMIMEObject, receiver):
    messageMIMEObject["To"] = receiver
    return messageMIMEObject.as_string()


def create_server(smtp, port, email, password):
    context = ssl.create_default_context()
    server = smtplib.SMTP(smtp, port)
    print("-- Defined server")
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(email, password)
    print("-- Logged")
    return server


def send_email(smtp, receiver_email, message):
    try:
        smtp.sendmail(config.EMAIL_ADDRESS, receiver_email, message)
        print("-- Mail Sended to: ", receiver_email)
    except Exception as e:
        # Print any error messages to stdout
        print(e)


def close_server(smtp):
    smtp.quit()
    
    

if __name__ == "__main__":
    main()












