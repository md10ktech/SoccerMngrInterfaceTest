import logging


class Logger:
    def __init__(self, test_name):
        self.logger = logging.getLogger(test_name)
        self.logger.setLevel(logging.INFO)
        self.console_handler = logging.StreamHandler()
        # self.console_handler.setLevel(logging.INFO)
        # green = "\x1b[31;32m" + "%(message)s" + "\x1b[0m"
        blue = "\x1b[31;34m" + "%(message)s" + "\x1b[0m"
        self.console_handler.setFormatter(logging.Formatter(blue, datefmt='%m/%d/%Y %I:%M:%S%p'))
        self.logger.addHandler(self.console_handler)
        # self.logger.propagate = False

    def log_info(self, log):
        self.logger.info(log)
