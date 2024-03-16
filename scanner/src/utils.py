import logging, sys

class SingletonLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logger = logging.getLogger('scanner')
            cls._instance.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            cls._instance.logger.setFormatter(formatter)
            cls._instance.logger.addHandler(logging.StreamHandler(sys.stdout))
        return cls._instance

    def __getattr__(self, name):
        return getattr(self.logger, name)

    def __setattr__(self, name, value):
        setattr(self.logger, name, value)

    def __delattr__(self, name):
        delattr(self.logger, name)