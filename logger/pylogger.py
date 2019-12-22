import logging
from logging import handlers
import time
import sys
from datetime import datetime

class Logger:
    def __init__(self, name=None, level=logging.WARNING, 
        stdout=True, file=False, 
        rotating_file=False, 
        timed_rotating_file=False):
        self.logger = logging.getLogger(name or __name__)
        self.logger.setLevel(level)

        if stdout:
            self.__init_Stream()
        if file:
            self.__init_File()
        if rotating_file:
            self.__init_RotatingFile()
        if timed_rotating_file:
            self.__init_TimedRotatingFile()

    
    def __init_Stream(self):
        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(logging.DEBUG)
        streamFormat = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        streamHandler.setFormatter(streamFormat)
        self.logger.addHandler(streamHandler)

    def __init_File(self, filepath='./out.log'):
        fileHandler = logging.FileHandler(filepath)
        fileHandler.setLevel(logging.DEBUG)
        fileFormat = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        fileHandler.setFormatter(fileFormat)
        self.logger.addHandler(fileHandler)

    def __init_RotatingFile(self, filepath='./rotating_out.log'):
        rotatingFileHandler = handlers.RotatingFileHandler(filepath, maxBytes=1e6)
        rotatingFileHandler.setLevel(logging.DEBUG)
        fileFormat = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        rotatingFileHandler.setFormatter(fileFormat)
        self.logger.addHandler(rotatingFileHandler)

    def __init_TimedRotatingFile(self, filepath='./timed_rotating_out.log'):
        timedRotatingFileHandler = handlers.TimedRotatingFileHandler(filepath, when='H', interval=1)
        timedRotatingFileHandler.setLevel(logging.DEBUG)
        fileFormat = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        timedRotatingFileHandler.setFormatter(fileFormat)
        self.logger.addHandler(timedRotatingFileHandler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg, exc_info=False):
        self.logger.error(msg, exc_info=exc_info)

    def critical(self, msg):
        self.logger.critical(msg)
    
    def exception(self, msg):
        self.logger.exception(msg)


def main():
    logger = Logger()
    logger.info('test')
    a = 5
    b = 0
    try:
        c = a/b
    except Exception as e:
        logger.error('Error: %s' % e, True)

if __name__ == "__main__":
    main()