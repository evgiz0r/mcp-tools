#!/usr/bin/env python3
"""
Test script for the MCP Server
This demonstrates how the MCP server handles tool calls
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pss_parser import parse_pss


def test_mcp_tool_interface():
    """Simulate MCP tool call interface."""
    
    test_cases = [
        {
            "name": "Valid PSS code",
            "code": """component pss_top {
    action A {};
    action B {};
    action C {
        activity {
            do A;
            do B;
        }
    }
    action D {
        activity {
            do C;
            do C;
        }
    }    
    action test {
        activity {
            do A;
            do B;
            do C;
            do D;
        }
    }
}"""
        },
        {
            "name": "Simple actions only",
            "code": """component pss_top {
    action A {};
    action B {};
}"""
        },
        {
            "name": "Invalid syntax",
            "code": "component pss_top { invalid }"
        }
    ]
    
    for test in test_cases:
        print("=" * 70)
        print(f"Test: {test['name']}")
        print("=" * 70)
        
        # Simulate MCP tool call
        result = parse_pss(test["code"])
        
        # Output as it would appear to MCP client
        print(json.dumps(result, indent=2))
        print()


if __name__ == "__main__":
    test_mcp_tool_interface()
