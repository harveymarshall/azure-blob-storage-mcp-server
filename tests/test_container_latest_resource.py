import sys
from unittest.mock import MagicMock, patch

# Mock the mcp module before importing server.main
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

# Now we can import from server.main
from server.main import containers_latest

TEST_LIST = [
    {
        "account": "test_account",
        "container": "container_1"
    }
]

def test_container_latest_resource():
    # Test with non-empty list
    output = containers_latest(TEST_LIST)
    assert output == TEST_LIST
    assert isinstance(output, list)

    # Test with empty list
    empty_output = containers_latest([])
    assert empty_output == "No recent container names or accounts to show"

    # Test default parameter behavior (empty CONTAINERS_ACCOUNTS)
    default_output = containers_latest()
    assert default_output == "No recent container names or accounts to show"
