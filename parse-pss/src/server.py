"""
MCP Server for PSS Parser Tool
"""

import json
import sys
from typing import Any

from pss_parser import parse_pss


class PSSerr(Exception):
    """Server error."""
    pass


def handle_parse_pss(text: str) -> dict[str, Any]:
    """
    Handle the parse_pss tool call.
    
    Args:
        text: PSS source code to parse
        
    Returns:
        Parsed result or error information
    """
    if not isinstance(text, str):
        return {
            "success": False,
            "error": "Input 'text' must be a string"
        }
    
    result = parse_pss(text)
    return result


def main():
    """
    Simple stdio-based MCP server for testing.
    In production, this would use the official MCP SDK.
    """
    print("PSS Parser MCP Server started.", file=sys.stderr)
    
    # For now, read a single line of input and process it
    # A real MCP server would use the SDK for proper protocol handling
    try:
        line = input()
        request = json.loads(line)
        
        if request.get("method") == "parse_pss":
            result = handle_parse_pss(request.get("params", {}).get("text", ""))
            response = {"jsonrpc": "2.0", "id": request.get("id"), "result": result}
        else:
            response = {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {"code": -32601, "message": "Method not found"}
            }
        
        print(json.dumps(response))
    except Exception as e:
        print(json.dumps({
            "jsonrpc": "2.0",
            "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
        }))


if __name__ == "__main__":
    main()
