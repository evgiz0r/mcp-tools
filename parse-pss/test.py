"""
Standalone test script for PSS Parser
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pss_parser import parse_pss


def test_parse_pss():
    """Test the PSS parser with the example input."""
    
    test_input = """component pss_top {
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
    
    print("=" * 60)
    print("PSS Parser Test")
    print("=" * 60)
    print("\nInput PSS Code:")
    print(test_input)
    print("\n" + "=" * 60)
    print("Parse Result (JSON):")
    print("=" * 60)
    
    result = parse_pss(test_input)
    print(json.dumps(result, indent=2))
    
    if result["success"]:
        print("\n✓ Parsing successful!")
        return True
    else:
        print(f"\n✗ Parsing failed: {result['error']}")
        return False


def test_error_cases():
    """Test error handling."""
    
    test_cases = [
        ("Duplicate action", "component pss_top { action A {} action A {} }"),
        ("Invalid syntax", "component pss_top { invalid }"),
        ("Missing component name", "component { action A {} }"),
    ]
    
    print("\n" + "=" * 60)
    print("Error Handling Tests")
    print("=" * 60)
    
    for desc, code in test_cases:
        print(f"\nTest: {desc}")
        print(f"Code: {code}")
        result = parse_pss(code)
        if not result["success"]:
            print(f"✓ Correctly caught error: {result['error']}")
        else:
            print(f"✗ Should have failed but succeeded")


if __name__ == "__main__":
    success = test_parse_pss()
    test_error_cases()
    sys.exit(0 if success else 1)
