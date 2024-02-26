from fastapi import HTTPException
from src.utils import handle_file_submission
import pytest

class MockUploadFile:
    def __init__(self, content):
        self.content = content

    async def read(self):
        return self.content
    
    def seek(self, offset):
        return self.content[offset]

class TestHandleFileSubmission:
    @pytest.mark.asyncio
    async def test_with_data_input(self):
        data = "test_data"
        key, content = await handle_file_submission(data=data)

        assert isinstance(key, str)
        assert isinstance(content, bytes)
        assert content == b"test_data"

    @pytest.mark.asyncio
    async def test_with_file_input(self):
        file_content = b"test_file_content"
        file = MockUploadFile(file_content)
        key, content = await handle_file_submission(file=file)

        assert isinstance(key, str)
        assert isinstance(content, bytes)
        assert content == file_content

    @pytest.mark.asyncio
    async def test_with_no_input(self):
        with pytest.raises(HTTPException) as exc_info:
            await handle_file_submission()
        assert exc_info.value.status_code == 400
        assert "No data or file provided" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_with_both_inputs(self):
        file_content = b"test_file_content"
        file = MockUploadFile(file_content)
        data = "test_data"
        with pytest.raises(HTTPException) as exc_info:
            await handle_file_submission(file=file, data=data)
        assert exc_info.value.status_code == 400
        assert "Provide data OR file" in str(exc_info.value.detail)
