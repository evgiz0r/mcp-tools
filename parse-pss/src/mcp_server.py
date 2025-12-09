#!/usr/bin/env python3
"""
PSS Parser MCP Server
A proper MCP (Model Context Protocol) server for parsing PSS code.
This server can be integrated with VS Code Copilot and other MCP clients.
"""

import json
import sys
import asyncio
from typing import Any

from mcp.server import Server
from mcp.types import Tool, TextContent, ToolResult

from pss_parser import parse_pss


# Create MCP server instance
server = Server("pss-parser-server")


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> ToolResult:
    """Handle tool calls from the MCP client."""
    
    if name == "parse_pss":
        pss_code = arguments.get("code", "")
        
        if not isinstance(pss_code, str):
            return ToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps({
                        "success": False,
                        "error": "Parameter 'code' must be a string"
                    }, indent=2)
                )],
                is_error=True
            )
        
        # Parse the PSS code
        result = parse_pss(pss_code)
        
        return ToolResult(
            content=[TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )],
            is_error=not result.get("success", False)
        )
    
    return ToolResult(
        content=[TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "error": f"Unknown tool: {name}"
            })
        )],
        is_error=True
    )


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="parse_pss",
            description="Parse PSS (Protocol State System) code and return structured JSON. "
                       "Accepts PSS component definitions with actions and activities. "
                       "Returns detailed error information on parse failure.",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "PSS source code to parse. "
                                      "Must be a valid component definition with actions."
                    }
                },
                "required": ["code"]
            }
        )
    ]


async def main():
    """Run the MCP server."""
    async with server:
        print("PSS Parser MCP server started on stdio", file=sys.stderr)
        print("Ready to accept tool calls", file=sys.stderr)
        await server.wait_for_shutdown()


if __name__ == "__main__":
    asyncio.run(main())
