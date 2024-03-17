import logging, sys

class SingletonLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Directly set attributes on the instance to avoid recursion
            object.__setattr__(cls._instance, 'logger', logging.getLogger('scanner'))
            cls._instance.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formatter)
            cls._instance.logger.addHandler(handler)
        return cls._instance

    def __getattr__(self, name):
        return getattr(object.__getattribute__(self, 'logger'), name)

    def __setattr__(self, name, value):
        setattr(object.__getattribute__(self, 'logger'), name, value)

    def __delattr__(self, name):
        delattr(object.__getattribute__(self, 'logger'), name)