from fastapi import HTTPException, Request
from starlette.datastructures import FormData
from src.utils import handle_file_submission
import pytest
from unittest.mock import Mock, AsyncMock

class MockUploadFile:
    def __init__(self, content):
        self.content = content

    async def read(self):
        return self.content
    
    async def seek(self, offset):
        pass

async def mock_request(data=None, file=None):
    form_data = {}
    if data:
        form_data['data'] = data
    if file:
        form_data['file'] = file

    request = Mock()
    request.form = AsyncMock(return_value=form_data)
    return request

@pytest.mark.asyncio
class TestHandleFileSubmission:

    async def test_with_data_input(self):
        data = "test_data"
        request = await mock_request(data=data)
        key, content = await handle_file_submission(request)

        assert isinstance(key, str)
        assert isinstance(content, bytes)
        assert content == b"test_data"

    
    async def test_with_file_input(self):
        file_content = b"test_file_content"
        file = MockUploadFile(file_content)
        request = await mock_request(file=file)
        key, content = await handle_file_submission(request)

        assert isinstance(key, str)
        assert isinstance(content, bytes)
        assert content == file_content

    
    async def test_with_no_input(self):
        request = await mock_request()
        with pytest.raises(HTTPException) as exc_info:
            await handle_file_submission(request)
        assert exc_info.value.status_code == 400
        assert "No data or file provided" in str(exc_info.value.detail)

    
    async def test_with_both_inputs(self):
        file_content = b"test_file_content"
        file = MockUploadFile(file_content)
        data = "test_data"
        request = await mock_request(file=file, data=data)
        with pytest.raises(HTTPException) as exc_info:
            await handle_file_submission(request)
        assert exc_info.value.status_code == 400
        assert "Provide data OR file" in str(exc_info.value.detail)
