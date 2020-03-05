import subprocess
import json
import logging

from MailData import MailData
from MailBox import MailBox
from MailHandlerInterface import MailHandlerInterface


class CommandHandler(MailHandlerInterface):
    """ This handler is called for every unread message """
    mailbox = None
    version = 0x0001 # high|low
    authorized_emails = []
    
    def __init__(self, mailbox, config_file):
        self.logger = logging.getLogger(self.logger_name + '.CMD')

        high = ((self.version&0xff00) >> 8)
        low =  (self.version&0xff)
        self.logger.debug('command handler init version {}.{}'.format(high,low))
    
        self.mailbox = mailbox

        try:
            # emails authorized to receive replies are at json file in the format:
            #{
            #"authorized_to_reply":[ "someone@email.com", "someonelse@email.com" ]
            #}
            self.logger.debug('trying to open the config file "{}"'.format(config_file))
            fd = open(config_file, 'r')
            self.authorized_emails = json.load(fd)['authorized_to_reply']
        except Exception as e:
            self.logger.error(e)
            pass

        self.logger.debug('emails authorized to receive replies: "{}"'.format(self.authorized_emails))

    def is_a_command(self, subject):
        return (len(subject) > 0) and (subject[0] == '$')

    def is_sender_valid(self, senderEmail):
        return (senderEmail in self.authorized_emails)
    
    def handle(self, mailData):
        self.logger.debug('handling possible command: "{}"'.format(mailData))

        name, sender = mailData.sender[0]
        name, destination = mailData.destination[0]
        self.logger.debug('sender "{}"'.format(sender))

        if not self.is_sender_valid(sender):
            self.logger.info('"{}" is not authorized to receive replies. This email will not be handled.'.format(sender))
            return
        else:
            self.logger.info('"{}" allowed to receive replies'.format(sender))

        if self.is_a_command(mailData.subject):
            cmd = mailData.subject[1:].split()
            self.logger.debug('command: "{}"'.format(cmd))

            output = subprocess.run(cmd,universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            newMail = MailData()
            newMail.subject = 'Re: ' + mailData.subject
            newMail.sender = destination
            newMail.destination = sender
            newMail.body = output.stdout + '\n' + output.stderr + '\n' + str(output.returncode)

            #newMail.attachments.append("C:/Users/user/Desktop/automation/hello.png")
            #newMail.attachments.append("C:/Users/user/Desktop/automation/email_settings.ini")
            #newMail.attachments.append("C:/Users/user/Desktop/automation/some_zip.zip")

            self.logger.debug('sending mail...')
            self.mailbox.send_email(newMail)

        else:
            newMail = MailData()
            newMail.subject = 'Re: ' + mailData.subject
            newMail.sender = destination
            newMail.destination = sender
            newMail.body = 'Thank you!'

            self.logger.debug('sending mail...')
            self.mailbox.send_email(newMail)



