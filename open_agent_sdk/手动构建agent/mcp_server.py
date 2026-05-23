import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MCP Server")

@mcp.tool()
def ls():
    """列出当前目录下的文件和文件夹。"""
    return os.listdir(".")

if __name__ == "__main__":
    mcp.run()