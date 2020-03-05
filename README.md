# MailBox

Send and receive emails using python scripts. Working so far using a Gmail account and python 3.

### What for? 
You can register handlers to parse new arrived messages, so you can for example run a command sent by mail (useful to me to automatize some stuff).
See `CommandHandler.py` for an example (also `CommandHandlerConfigs.json`).
See `Main.py` for how to register a new handler and control the main loop.

In the given example, `CommandHandler.py` parses the received mail. If the subject starts with `$` and the sender is an authorized email, a reply email will be sent with the command output (send an email with subject "$ping google.com", for example).

### Instalation
Python 3 dependencies can be installed using pip: `pip install pyzmail36 imapclient`.


### Usage
1. Setup `email_settings.ini` with IMAP and SMTP server addresses and port. Inform also your username and password.
2. Setup `CommandHandlerConfigs.json` with a valid email address (allowed to receive replies from the script).

### Development Status
Basically functionality is achieved, but it is not capable to reply binary attachments yet.
And it is likelly to stay like this because I don't have time to continue :(

