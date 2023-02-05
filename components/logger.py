import logging


class Logger:
    logger = None

    @staticmethod
    def init(name, file):
        Logger.logger = logging.getLogger(name)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%H:%M:%S')

        f_handler = logging.FileHandler(file)
        f_handler.setLevel(logging.INFO)
        f_format = logging.Formatter(fmt='%(asctime)s - %(levelname)s: %(message)s', datefmt='%H:%M:%S')
        f_handler.setFormatter(f_format)

        Logger.logger.addHandler(f_handler)

    @staticmethod
    def info(msg):
        Logger.logger.info(msg)

    @staticmethod
    def error(msg):
        Logger.logger.error(msg)
