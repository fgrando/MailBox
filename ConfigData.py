
import os
import configparser

class ConfigData:
    """ Email client configuration data loader """
    username = None
    password = None
    imap = None
    imap_port = None
    smtp = None
    smtp_port = None
    ssl_enabled = None
    settings = None

    def __init__(self, config_file):
        self.settings = config_file
        self.load(self.settings)

    def load(self, filename):
        success = False
        username_label = 'username'
        password_label = 'password'
        credentials_label = 'credentials'
        imap_label = 'imap'
        imap_port_label = 'imap_port'
        smtp_label = 'smtp'
        smtp_port_label = 'smtp_port'
        ssl_label = 'usessl'

        parser = configparser.ConfigParser()
        if not os.path.exists(filename):
            print("Credentials file not found!")
            msg = """This file should be named '{}' with the following data:
                    [{}]
                    {}=your@email.com
                    {}=yourpass
                    {}=email.server.com
                    {}=993
                    {}=smtp.server.com
                    {}=465
                    {}=True"""
            print(msg.format(filename,\
                            credentials_label,\
                            username_label,\
                            password_label,\
                            imap_label,\
                            imap_port_label,\
                            smtp_label,\
                            smtp_port_label,\
                            ssl_label))
        else:
            parser.read(filename)

            self.username = parser[credentials_label][username_label]
            self.password = parser[credentials_label][password_label]
            self.imap = parser[credentials_label][imap_label]
            self.smtp = parser[credentials_label][smtp_label]
            self.imap_port = int(parser[credentials_label][imap_port_label])
            self.smtp_port = int(parser[credentials_label][smtp_port_label])
            self.ssl_enabled = \
                            ((parser[credentials_label][ssl_label] == "True") or\
                            (parser[credentials_label][ssl_label] == "true"))
            success = True

        return success


    def toString(self):
        s = "'{}' '{}' '{}' '{}' '{}' '{}' '{}' '{}' '{}'".format(
            self.settings,\
            self.username,\
            self.password,\
            self.imap,\
            self.imap_port,\
            self.smtp,\
            self.smtp_port,\
            self.ssl_enabled)
        return s

    def toStringFiltered(self):
        s = "'{}' '{}' '{}' '{}' '{}' '{}' '{}'".format(
            self.settings,\
            self.username,\
            self.imap,\
            self.imap_port,\
            self.smtp,\
            self.smtp_port,\
            self.ssl_enabled)
        return s

    def __str__(self):
        return self.toString()


    def __repr__(self):
        return self.toString()

