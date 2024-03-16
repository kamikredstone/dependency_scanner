import uuid
from fastapi import UploadFile, HTTPException, Request
from starlette.datastructures import FormData
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


async def handle_file_submission(request: Request = None) -> tuple[str, bytes]:
    logger = SingletonLogger()
    form_data: FormData = await request.form()
    file: UploadFile = form_data.get("file")
    data = form_data.get("data")
    if not data and not file:
        logger.error("No data or file provided")
        raise HTTPException(status_code=400, detail="No data or file provided")
    elif data and file:
        logger.error("Both data and file were provided")
        raise HTTPException(status_code=400, detail="Provide data OR file not both")
    
    key = str(uuid.uuid4())
    if data:
        logger.info('Received data, starting processing...')
        content = data.encode()
    elif file:
        logger.debug('Received file, starting processing...')
        await file.seek(0)
        content = await file.read()
    return key, content