import uuid
from fastapi import UploadFile, HTTPException, Request
from starlette.datastructures import FormData
import logging, sys


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

async def handle_file_submission(request: Request = None) -> tuple[str, bytes]:
    form_data: FormData = await request.form()
    file: UploadFile = form_data.get("file")
    data = form_data.get("data")
    if not data and not file:
        raise HTTPException(status_code=400, detail="No data or file provided")
    elif data and file:
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