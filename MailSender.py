import logging
import smtplib
import mimetypes
import os
import base64
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


# my stuff
from MailLog import MailLog
from MailData import MailData


class MailSender(MailLog):
    """ Client to send emails """
    username = None
    password = None
    smtp_host = None
    smtp_port = None
    
    def __init__(self, smtp_host, smtp_port, username, password):
        self.logger = logging.getLogger(self.logger_name + '.MailSender')
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        
    def send(self, emailData):
        #self.logger.debug('building email "{}"'.format(emailData))
        self.logger.debug('building email...'.format(emailData))
        msg = MIMEMultipart()
        msg['Subject'] = emailData.subject
        msg['From'] = emailData.sender
        msg['To'] = emailData.destination
        
        txt = MIMEText(emailData.body)
        msg.attach(txt)
        self.logger.debug('added message "{}"'.format(txt))

        for a in emailData.attachments:
            self.logger.debug('attaching "{}"'.format(a))
            self.load_attachment(a, msg)

        server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
        
        self.logger.debug("login started")
        server.login(self.username, self.password)

        self.logger.debug("encoding message")
        mail_ascii = msg.as_string().encode('ascii', 'ignore').decode('ascii')

        self.logger.debug("sending mail")
        server.sendmail(emailData.sender, emailData.destination, mail_ascii)

        server.quit()
        self.logger.debug("email sent")

        
    def load_attachment(self, filepath, message):

        msg = None
        content_type, encoding = mimetypes.guess_type(filepath)
        
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(filepath, 'rb')
            msg = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(filepath, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(filepath, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(filepath, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()
        filename = os.path.basename(filepath)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)
        
        
        
        #    with open(a, 'rb') as f:
        #        img = MIMEImage(f.read())
        #    img.add_header('Content-Disposition',
        #                'attachment',
        #                filename=os.path.basename(a))
        #    msg.attach(img)
        
        self.logger.debug("{} is not supported yet".format(filepath))
        
        #fd = open(a, 'rb')
        #
        #msg = MIMEBase(main_type, sub_type)
        #msg.set_payload(base64.b64encode(fd.read()))
        #filename = os.path.basename(file_path)
        #msg.add_header('Content-Disposition', 'attachment', filename=filename)

        #filepath = '/path/to/image/file'
        #with open(filepath, 'rb') as f:
        #    img = MIMEImage(f.read())
        #
        #img.add_header('Content-Disposition',
        #            'attachment',
        #            filename=os.path.basename(filepath))
        #msg.attach(img)

    def create_message_with_attachment(
        sender, to, subject, message_text, file):
        """Create a message for an email.
        
        Args:
            sender: Email address of the sender.
            to: Email address of the receiver.
            subject: The subject of the email message.
            message_text: The text of the email message.
            file: The path to the file to be attached.
        
        Returns:
            An object containing a base64url encoded email object.
        """
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        
        msg = MIMEText(message_text)
        message.attach(msg)
        
        content_type, encoding = mimetypes.guess_type(file)
        
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(file, 'rb')
            msg = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(file, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(file, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(file, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()
        filename = os.path.basename(file)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)
        
        return {'raw': base64.urlsafe_b64encode(message.as_string())}
