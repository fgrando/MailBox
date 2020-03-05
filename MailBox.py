import logging
import os
import shutil

# my stuff
from MailLog import MailLog
from MailSender import MailSender
from MailReceiver import MailReceiver
from ConfigData import ConfigData


class MailBox(MailLog):
    """ Email client that download unread messages and process them using registered handlers """
    handlers = []
    configs = None
    workspace = None
    
    receiver = None # receiver engine
    sender = None # send engine

    def __init__(self, config_file, workspace_folder):
        self.logger = logging.getLogger(self.logger_name + '.MailBox')
        self.workspace = workspace_folder
        self.configs = ConfigData(config_file)

        self.logger.debug('workspace "{}" configs: {}'.format(self.workspace, self.configs.toStringFiltered()))
        
        self.logger.debug('creating MailReceiver')
        self.receiver = MailReceiver(self.configs.imap,\
                                     self.configs.imap_port,\
                                     self.configs.ssl_enabled,\
                                     self.configs.username,\
                                     self.configs.password)

        self.logger.debug('creating MailSender')
        self.sender = MailSender(self.configs.smtp,\
                                self.configs.smtp_port,\
                                self.configs.username,\
                                self.configs.password)



    def process_unread_messages(self):
        workspace = os.path.join(self.workspace,"") #workspace is used to download attachments, if any
        unread_mails = self.receiver.get_unread_mails(workspace)
        for email in unread_mails:
            self.logger.debug('processing email [{}]'.format(email))
            
            # call all handlers to process it
            for h in self.handlers:
                try:
                    self.logger.debug('handler {} called'.format(self.handlers.index(h)))
                    h.handle(email)
                except Exception as e:
                    self.logger.error(e)
                    pass
            
            # remove the temporary directory
            self.logger.debug('removing temporary directory "{}"'.format(email.workspace))
            shutil.rmtree(email.workspace)

            # set as unread
            self.receiver.set_as_read(email)


    def send_email(self, mailData):
        self.logger.debug('sending email...')
        self.sender.send(mailData)
        self.logger.debug('sending complete')

    def add_mailbox_handler(self, handler):
        self.handlers.append(handler)
        self.logger.debug('added handler "{}"'.format(handler))

