import uuid
from fastapi import File, UploadFile, HTTPException, Request

async def handle_file_submission(data: Request = None, file: UploadFile = None) -> tuple[uuid.uuid4, bytes]:
    ## TODO: handle a case where there is both file and data
    if not data and not file:
        raise HTTPException(status_code=400, detail="No data or file provided")
    elif data and file:
        raise HTTPException(status_code=400, detail="Provide data OR file")
    key = str(uuid.uuid4())
    if data:
        content = await data.body()
    elif file:
        await file.seek(0)
        content = await file.read()
    return key, content