import logging
import os
from imapclient import IMAPClient
import pyzmail
import tempfile


# my stuff
from MailData import MailData
from MailLog import MailLog

class MailReceiver(MailLog):
    """ Client to receive emails """
    imap = None

    def __init__(self, imap_host, imap_port, ssl_enabled, username, password):
        self.logger = logging.getLogger(self.logger_name + '.MailReceiver')

        self.logger.debug('creating imap client')
        self.imap = IMAPClient(imap_host,\
                                port=imap_port,\
                                use_uid=True,\
                                ssl=ssl_enabled)
        try:
            self.logger.debug('doing imap login')
            self.imap.login(username, password)
        except Exception as e:
            error = """Failed to login! Please check the data:
                        host: {}
                        port: {}
                        ssl : {}
                        user: {}
                        pass: {}"""
            print(error.format(imap_host, imap_port, ssl_enabled, username, password))
            self.logger.error(e)
            pass
        self.logger.debug('init complete')

    def get_unread_mails(self, workspace):
        self.imap.select_folder('INBOX', readonly=True)

        messages_ids = self.imap.search([b'NOT', b'SEEN']) # UNSEEN
        messages = self.imap.fetch(messages_ids, data=['BODY[]'])
        self.logger.debug('{} unread messages'.format(len(messages)))

        # enable writing so we can do some changes later
        self.imap.select_folder('INBOX', readonly=False)

        unread_mails = []

        # for every unread message, download the email and call the handlers
        for msg_id, content in messages.items():
            email = pyzmail.PyzMessage.factory(content[b'BODY[]'])
            data = MailData()
            data.id = msg_id
            data.subject = email.get_subject()
            data.sender = email.get_addresses('from')
            data.destination = email.get_addresses('to')
            
            # be sure that the prefix will end with a slash
            workspace = os.path.join(workspace,"")
            data.workspace = tempfile.mkdtemp(prefix=workspace)

            # load the email data with the downloaded parts
            for p in email.mailparts:
                if self.is_body(p):
                    data.body = p.get_payload().decode(p.charset)
                elif self.is_attachment(p):
                    data.attachments.append(p.filename)
                    if self.save_attachment(data.workspace,p):
                        data.attachments_saved.append(p.filename)
            
            unread_mails.append(data)
        return unread_mails

    def set_as_read(self, mailData):
        self.logger.debug('setting email "{}" as read'.format(mailData.id))
        self.imap.add_flags(mailData.id, ['\\Seen','\\Answered'])
        
    def save_attachment(self, workspace, mailpart):
        filename = mailpart.filename
        destination = os.path.join(workspace, filename)
        self.logger.debug('saving attachment "{}" to {}'.format(filename, destination))
        try:
            fp = open(destination, 'wb')
            fp.write(mailpart.get_payload())
            fp.close()
            return True

        except Exception as e:
            self.logger.error(e)
            pass

        return False

    def is_attachment(self, mailpart):
        result = ((mailpart.filename != None) and (mailpart.charset == None))
        self.logger.debug('"{}" is attachment? {}'.format(mailpart.filename, result))
        return result

    def is_body(self, mailpart):
        return ((mailpart.filename == None) and (mailpart.is_body == "text/plain"))
