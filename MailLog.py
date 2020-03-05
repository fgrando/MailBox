import logging

class MailLog:
    logger_name = "MailLog"
    
#
# create the logger
#    how to at: https://docs.python.org/3/howto/logging-cookbook.html
#
logger_name = MailLog.logger_name
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(logger_name+'.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s-%(levelname)s: %(message)s')
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)