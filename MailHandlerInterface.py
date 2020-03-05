from MailLog import *

class MailHandlerInterface(MailLog):
    """Inherit this class in your handler so it will be called to treat unread messages."""
    name = None
    
    def handle(self, mailData):
        msg = "This is the default handler and will do nothing with the downloaded message: {}"
        print(msg.format(mailData))


