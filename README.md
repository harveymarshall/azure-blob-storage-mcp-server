# Azure Blob Storage MCP Server

This project provides an MCP server for interacting with Azure Blob Storage using the MCP protocol. You can connect this server to clients like Claude Desktop for natural language access to your Azure Blob Storage resources.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/azure-blob-storage-mcp-server.git
cd azure-blob-storage-mcp-server
```

### 2. Go to you AI Agent

- Add this to the settings in your AI Agent

```json
"Azure-Blob-Storage-MCP-Server": {
    "command": "uv",
    "args": [
      "run",
      "--with",
      "mcp[cli]",
      "--with",
      "azure-storage-blob",
      "--with",
      "azure-identity",
      "mcp",
      "run",
      "{path/to/where/you/cloned/the/repository}azure-blob-storage-mcp-server/server/main.py"
    ]
  }
```

## Notes

- Ensure your Azure credentials are valid and have access to the target storage account. (run az login from your terminal)
- Ensure you have read/write access for the storage accounts / containers / blobs you are accessing
- You may need to adjust firewall or network settings if connecting from another device.
- For more information on MCP protocol or Claude Desktop, refer to their respective documentation.
