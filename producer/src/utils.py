import uuid
from fastapi import UploadFile, HTTPException, Request
from starlette.datastructures import FormData
import logging, sys

class SingletonLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Directly set attributes on the instance to avoid recursion
            object.__setattr__(cls._instance, 'logger', logging.getLogger('producer'))
            cls._instance.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formatter)
            cls._instance.logger.addHandler(handler)
        return cls._instance

    def __getattr__(self, name):
        # Safely delegate attribute access to the logger
        return getattr(object.__getattribute__(self, 'logger'), name)

    def __setattr__(self, name, value):
        # Safely delegate attribute setting to the logger
        setattr(object.__getattribute__(self, 'logger'), name, value)

    def __delattr__(self, name):
        # Safely delegate attribute deletion to the logger
        delattr(object.__getattribute__(self, 'logger'), name)

def detect_programming_language(filename: str) -> str:
    """
    This function detects the programming language of the manifest file based on the file name.
    """
    # Mapping of file names to programming languages
    language_mapping = {
        'requirements.txt': 'python',
        'package.json': 'javascript',
        # Add more mappings here as needed
    }
    for file_identifier, language in language_mapping.items():
        if filename.endswith(file_identifier):
            return language
    return 'unknown'  # Default if no match is found


async def handle_file_submission(request: Request = None) -> tuple[str, dict[str, str]]:
    """
    This function handles the file submission request and returns the key and content.

    Args:
        request (Request): The request object containing the file or data.

    Returns:
        tuple[str, dict[str, str]]: A tuple containing the key as UUID identifier,
            and a dictionary with the key representing the programming language 
            and content of the manifest file as the value.

    """
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
        # TODO: Add detection for language in case of simple string data
        logger.info('Received data, starting processing...')
        content = {'data': data.encode()}
        language = 'data'
    elif file:
        logger.debug(f'Received file {file.filename}, starting processing...')
        await file.seek(0)
        content = await file.read()
        language = detect_programming_language(file.filename)
    return key, {language: content}