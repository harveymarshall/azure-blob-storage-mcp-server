import sys
from unittest.mock import MagicMock, patch
import os

# Mock the mcp and azure modules before importing server.main
sys.modules['mcp'] = MagicMock()
sys.modules['mcp.server'] = MagicMock()
sys.modules['mcp.server.fastmcp'] = MagicMock()
sys.modules['azure'] = MagicMock()
sys.modules['azure.identity'] = MagicMock()
sys.modules['azure.storage'] = MagicMock()
sys.modules['azure.storage.blob'] = MagicMock()

# Create a proper FastMCP mock that returns decorators which preserve the original function
class MockFastMCP:
    def __init__(self, *args, **kwargs):
        pass  # Accept any arguments but don't do anything with them

    def tool(self, *args, **kwargs):
        return lambda func: func

    def resource(self, *args, **kwargs):
        return lambda func: func

# Ensure we override any existing mock
sys.modules['mcp.server.fastmcp'].FastMCP = MockFastMCP

# Clear any cached imports
if 'server.main' in sys.modules:
    del sys.modules['server.main']

from server.main import (
    create_container,
    list_containers,
    list_blobs,
    download_blobs,
    summarize_blob
)

def test_create_container():
    with patch('server.main.BlobServiceClient') as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.create_container.return_value = 'created'
        result = create_container('testaccount', 'testcontainer')
        assert result == 'created'
        mock_instance.create_container.assert_called_with('testcontainer')

def test_list_containers():
    with patch('server.main.BlobServiceClient') as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.list_containers.return_value = [
            {'name': 'container1'},
            {'name': 'container2'}
        ]
        result = list_containers('testaccount')
        assert result == ['container1', 'container2']

def test_list_blobs():
    with patch('server.main.BlobServiceClient') as MockClient:
        mock_instance = MockClient.return_value
        container_client = mock_instance.get_container_client.return_value
        container_client.list_blobs.return_value = [
            MagicMock(name='blob1'),
            MagicMock(name='blob2')
        ]
        # Patch blob.name property
        container_client.list_blobs.return_value[0].name = 'blob1.txt'
        container_client.list_blobs.return_value[1].name = 'blob2.txt'
        result = list_blobs('testaccount', 'testcontainer')
        assert result == ['blob1.txt', 'blob2.txt']

def test_download_blobs(tmp_path):
    with patch('server.main.BlobServiceClient') as MockClient:
        mock_instance = MockClient.return_value
        container_client = mock_instance.get_container_client.return_value
        blob_client = container_client.get_blob_client.return_value
        blob_client.download_blob.return_value.readall.return_value = b'data'
        blobs = ['file1.txt', 'file2.txt']
        result = download_blobs('testaccount', 'testcontainer', blobs, str(tmp_path))
        assert result['success']
        for blob in blobs:
            file_path = os.path.join(str(tmp_path), blob)
            assert os.path.exists(file_path)
            with open(file_path, 'rb') as f:
                assert f.read() == b'data'

def test_summarize_blob():
    with patch('server.main.BlobServiceClient') as MockClient:
        mock_instance = MockClient.return_value
        container_client = mock_instance.get_container_client.return_value
        blob_client = container_client.get_blob_client.return_value
        blob_client.download_blob.return_value.readall.return_value = b'hello world' * 100
        summary = summarize_blob('testaccount', 'testcontainer', 'blob1')
        assert summary.startswith('hello world')
        assert len(summary) <= 503  # 500 chars + '...'
