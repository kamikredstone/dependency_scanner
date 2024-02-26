import uuid
from fastapi import File, UploadFile, HTTPException

async def handle_file_submission(data: str = None, file: UploadFile = None) -> tuple[uuid.uuid4, bytes]:
    ## TODO: handle a case where there is both file and data
    if not data and not file:
        raise HTTPException(status_code=400, detail="No data or file provided")
    elif data and file:
        raise HTTPException(status_code=400, detail="Provide data OR file")
    key = str(uuid.uuid4())
    if data:
        content = data.encode()
    elif file:
        file.seek(0)
        content = await file.read()
    return key, content