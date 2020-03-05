#!/usr/bin/python

#
# In order to work you must:
#
# 1. allow less secure apps (in gmail): https://myaccount.google.com/lesssecureapps?pli=1
# 2. enable IMAP into your email configs
# 3. install: pip install pyzmail36 imapclient
#

#import logging
import time
from random import seed
from random import random


# Mailbox
from MailLog import *
from MailBox import *
from MailHandlerInterface import *

# Mailbox handlers:
from CommandHandler import *




logger.info('creating MailBox')
mb = MailBox('email_settings.ini', "C:/Users/user/Desktop/automation")

#
# register handlers to treat unread messages
#
mb.add_mailbox_handler(CommandHandler(mb, 'CommandHandlerConfigs.json'))
#mb.add_mailbox_handler(___here___)


# main loop
seed(1)
while True:
    logger.debug('checking mailbox')
    mb.process_unread_messages()
    wait_seconds = int(random()*100)%50 + 15


    logger.debug('waiting {} seconds'.format(wait_seconds))
    separator = ""
    for s in range(80):
        separator = separator + " ="
    logger.debug('cycle complete.' + separator + '\n\n')

    
    for i in range(wait_seconds):
        time.sleep(1) # did like this so Ctrl+C will work immediatelly

    

