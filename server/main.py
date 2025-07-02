# server.py
from mcp.server.fastmcp import FastMCP

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

CREDENTIAL = DefaultAzureCredential()

# Create an MCP server
mcp = FastMCP("Azure-Blob-Storage-MCP-Server")

CONTAINERS_ACCOUNTS = []

def client(account_name: str, credential: DefaultAzureCredential=CREDENTIAL) -> BlobServiceClient:
    blob_service_client = BlobServiceClient(f"https://{account_name}.blob.core.windows.net", credential)
    return blob_service_client

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
    client = client(account_name)
    create = client.create_container(container_name)
    return create

@mcp.tool(title="List Azure Blob Containers")
def list_containers(account_name: str) -> list:
    client = client(account_name)
    containers = client.list_containers()
    CONTAINERS_ACCOUNTS.clear()
    containers_list = []
    for container in containers:
        containers_list.append(container["name"])
        CONTAINERS_ACCOUNTS.append({"account": account_name, "container": container['name']})
    return containers_list

@mcp.resource("containers://latest")
def containers_latest() -> list:
    """_summary_

    Returns:
        list: list of objects showing the containers and the account they are associated with
    """
    if CONTAINERS_ACCOUNTS == {}:
        return "No recent container names or accounts to show"
    return CONTAINERS_ACCOUNTS


# Add a dynamic greeting resource
@mcp.tool(title="List Blobs")
def list_blobs(account_name: str, container_name: str) -> list:
    """Get a list of blobs within a container.

    Args:
        account_name (str): name of the storage account where we want to list blobs from a container
        container_name (str): name of the container within the storage account

    Returns:
        list: list of blobs within the container
    """
    client = client(account_name)
    container_client = client.get_container_client(container_name)
    blob_list = [blob.name for blob in container_client.list_blobs()]
    return blob_list

@mcp.tool(title="download_blobs")
def download_blobs(account_name: str, container_name: str, blobs: list, destination_folder: str = ".") -> dict:
    """Download blobs from names provided in the list

    Args:
        account_name (str): name of the storage account where we want to download blobs from a container
        container_name (str): name of the container within the storage account
        blobs (list): list of file names to download (should be blob names, not full paths)
        destination_folder (str): local folder to save downloaded files (default: current directory)
    Returns:
        dict: Summary of download results for each blob
    """
    import os
    results = []
    client = client(account_name)
    container_client = client.get_container_client(container_name)
    os.makedirs(destination_folder, exist_ok=True)
    for blob_name in blobs:
        try:
            blob_client = container_client.get_blob_client(blob_name)
            download_path = os.path.join(destination_folder, os.path.basename(blob_name))
            with open(download_path, "wb") as file:
                download_stream = blob_client.download_blob()
                file.write(download_stream.readall())
            results.append({"blob": blob_name, "status": "success", "path": download_path})
        except Exception as e:
            results.append({"blob": blob_name, "status": "error", "error": str(e)})
    overall_success = all(r["status"] == "success" for r in results)
    return {"success": overall_success, "results": results}

@mcp.tool(title="summarize_blob")
def summarize_blob(account_name: str, container_name: str, blob_name: str) -> str:
    """Read the contents of a blob into memory and return a summary (first 500 characters).

    Args:
        account_name (str): name of the storage account
        container_name (str): name of the container
        blob_name (str): name of the blob to summarize

    Returns:
        str: A summary (first 500 characters) of the blob's contents
    """
    client = client(account_name)
    container_client = client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    blob_data = blob_client.download_blob().readall()
    try:
        text = blob_data.decode("utf-8")
    except UnicodeDecodeError:
        return "Blob is not a UTF-8 text file."
    summary = text[:500]
    if len(text) > 500:
        summary += "..."
    return summary

