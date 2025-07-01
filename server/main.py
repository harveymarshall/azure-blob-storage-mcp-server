# server.py
from mcp.server.fastmcp import FastMCP

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

CREDENTIAL = DefaultAzureCredential()

# Create an MCP server
mcp = FastMCP("Azure-Blob-Storage-MCP-Server")


# Add an addition tool
@mcp.tool(title="Create Azure Blob Container")
def create_container(account_name: str, container_name: str):
    """Create a BlobServiceClient instance and create a new
    container.

    Args:
        account_name (str): name of the storage account to add new container.
        container_name (str): name of the new container.

    Returns:
        _type_: _description_
    """
    blob_service_client = BlobServiceClient(f"https://{account_name}.blob.core.windows.net", credential=CREDENTIAL)
    create = blob_service_client.create_container(container_name)
    return create

@mcp.tool(title="List Azure Blob Containers")
def list_containers(account_name: str) -> list:
    blob_service_client = BlobServiceClient(f"https://{account_name}.blob.core.windows.net", credential=CREDENTIAL)
    containers = blob_service_client.list_containers()
    containers_list = []
    for container in containers:
        containers_list.append(container["name"])
    return containers_list



# Add a dynamic greeting resource
@mcp.tool(title="List Blobs")
def list_blobs(account_name: str, container_name: str) -> list:
    """Get a list of blobs within a container.

    Args:
        account_name (str): name of the storage account where we want to list blobs from a container
        container_name (str): name of the container within the storage account

    Returns:
        list: _description_
    """
    blob_service_client = BlobServiceClient(f"https://{account_name}.blob.core.windows.net", credential=CREDENTIAL)
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = [blob.name for blob in container_client.list_blobs()]
    return blob_list
