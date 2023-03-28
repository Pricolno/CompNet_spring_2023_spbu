import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
import env
import sys

SENDER_MAIL = env.SENDER_MAIL
PASSWORD_SMTP =  env.PASSWORD_SMTP
RECIVER_MAIL = env.RECIVER_MAIL
PATH_TO_FILE = env.PATH_TO_FILE

SUBJECT = "TESTING SMTP MESSAGE"

def send_email():
    msg = MIMEMultipart()
    msg['From'] = SENDER_MAIL
    msg['To'] = RECIVER_MAIL
    msg['Subject'] = SUBJECT

    type = PATH_TO_FILE.split('.')[1]
    if type not in ['txt', 'html']:
        raise "file not txt/html"
    if type == 'txt':
        type = 'plain'
    
    BODY = None
    with open(PATH_TO_FILE) as file:
        BODY = file.read()

    message = MIMEText(BODY, type)
    msg.attach(message)
    try:
        mailserver = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
        # mailserver.set_debuglevel(True)
        mailserver.login(SENDER_MAIL, PASSWORD_SMTP)
        mailserver.sendmail(SENDER_MAIL, RECIVER_MAIL, msg.as_string())
        mailserver.quit()
        print("Письмо успешно отправлено")
    except smtplib.SMTPException:
        print("Ошибка: Невозможно отправить сообщение")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        SENDER_MAIL = input('Enter your email: ')
        PASSWORD_SMTP = input('Enter the password: ')
        RECIVER_MAIL =  input('Enter the destination email: ')
        PATH_TO_FILE = input('Enter the file txt/html for send: ')
    send_email()