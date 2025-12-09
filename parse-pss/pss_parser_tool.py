#!/usr/bin/env python3
"""
PSS Parser Tool - Callable interface for MCP
This module exposes the parse_pss function as a direct tool
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pss_parser import parse_pss


def parse_pss_tool(code: str) -> dict:
    """
    Parse PSS code and return JSON result.
    
    Args:
        code: PSS source code to parse
        
    Returns:
        Dictionary with parse result (success/error)
    """
    return parse_pss(code)


if __name__ == "__main__":
    # Simple CLI for testing
    if len(sys.argv) > 1:
        code = sys.argv[1]
    else:
        code = sys.stdin.read()
    
    result = parse_pss_tool(code)
    print(json.dumps(result, indent=2))
