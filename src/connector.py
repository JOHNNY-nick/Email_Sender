import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from .email_message import TextEmail

class SMTPConnectionError(Exception):
    pass

class  SMTPConnector() :
    """Cette classe permet d'intéragir avec le serveur SMTP"""
    def __init__(self) :
        load_dotenv()
        self.__email = os.environ.get('EMAIL_ADDRESS')
        self.__password = os.environ.get('EMAIL_PASSWORD')
        self.__host = os.environ.get('SMTP_HOST')
        self.__port = int(os.environ.get('SMTP_PORT'))
        self.__smtp = None 

    def __enter__(self) :
        
        try :
            self.__smtp = smtplib.SMTP_SSL(self.__host, self.__port)
            self.__smtp.login(self.__email,self.__password)
            return self
        
        except smtplib.SMTPAuthenticationError:
            raise SMTPConnectionError("Credentials invalides")

        except smtplib.SMTPConnectError:
            raise SMTPConnectionError("Serveur inaccessible")

    def __exit__(self, exc_type, exc, tb):
        if self.__smtp is not None :
            self.__smtp.quit()
        return False
    
    def send(self,message: TextEmail) :
        msg = MIMEMultipart()
        msg['From'] = self.__email
        msg['To'] = message.to
        msg['Subject'] = message.subject
        msg['Cc'] = ", ".join(message.cc)

        msg.attach(MIMEText(message.build_body(), 'plain'))

        for path in message.attachments :
            contenu = Path(path).read_bytes()
            cont = MIMEBase('application', 'octet-stream')
            cont.set_payload(contenu)
            encoders.encode_base64(cont)
            cont.add_header('Content-Disposition', 'attachment', filename = Path(path).name)
            msg.attach(cont)
        destinataires = [message.to] + message.cc
        self.__smtp.sendmail(
            self.__email,
            destinataires,
            msg.as_string()
        )