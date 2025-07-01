# Azure Blob Storage MCP Server

This project provides an MCP server for interacting with Azure Blob Storage using the MCP protocol. You can connect this server to clients like Claude Desktop for natural language access to your Azure Blob Storage resources.

## Getting Started

### 1. Clone the Repository

```bash
uv clone https://github.com/your-username/azure-blob-storage-mcp-server.git
cd azure-blob-storage-mcp-server
```

### 2. Set Up Python Environment

It's recommended to use a virtual environment. With uv, you can create and activate it as follows:

```bash
uv init
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
uv pip install -r pyproject.toml
```

### 4. Authenticate with Azure

Make sure you are authenticated with Azure so the MCP server can access your Blob Storage:

```bash
az login
```

### 5. Start the MCP Server

## Connecting to Claude Desktop

## Notes

- Ensure your Azure credentials are valid and have access to the target storage account.
- You may need to adjust firewall or network settings if connecting from another device.
- For more information on MCP protocol or Claude Desktop, refer to their respective documentation.
