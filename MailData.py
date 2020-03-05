class MailData:
    """ Data struct from some email"""
    subject = None
    sender = None
    destination = None
    body = None
    workspace = None
    attachments = []
    attachments_saved = []
    id = None

    def toString(self):
        s = "'{}' '{}' '{}' '{}' '{}' '{}' '{}' '{}'".format(
        self.id,\
        self.subject,\
        self.sender,\
        self.destination,\
        self.body,\
        self.workspace,\
        '.'.join(self.attachments),\
        '.'.join(self.attachments_saved))
        return s
        
    def __str__(self):
        return self.toString()
    
    def __repr__(self):
        return self.toString()