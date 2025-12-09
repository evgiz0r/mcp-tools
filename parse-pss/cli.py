#!/usr/bin/env python3
"""
PSS Parser CLI - Interactive tool to parse PSS code
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pss_parser import parse_pss


def main():
    """Interactive PSS parser CLI."""
    print("=" * 70)
    print("PSS Parser CLI Tool")
    print("=" * 70)
    print("\nOptions:")
    print("  1. Parse PSS code from stdin")
    print("  2. Parse PSS code from file")
    print("  3. Parse example")
    print("  4. Exit")
    print()
    
    while True:
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            print("\nEnter PSS code (enter 'END' on a new line when done):")
            lines = []
            while True:
                line = input()
                if line == "END":
                    break
                lines.append(line)
            code = "\n".join(lines)
            result = parse_pss(code)
            print_result(result)
            
        elif choice == "2":
            filepath = input("Enter file path: ").strip()
            try:
                with open(filepath, 'r') as f:
                    code = f.read()
                result = parse_pss(code)
                print_result(result)
            except FileNotFoundError:
                print(f"Error: File '{filepath}' not found")
            except Exception as e:
                print(f"Error: {e}")
                
        elif choice == "3":
            example = """component pss_top {
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
            print("\nParsing example PSS code:")
            print(example)
            result = parse_pss(example)
            print_result(result)
            
        elif choice == "4":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option. Please select 1-4.")


def print_result(result):
    """Pretty print the parse result as JSON."""
    print("\n" + "=" * 70)
    print("PARSE RESULT (JSON)")
    print("=" * 70)
    print(json.dumps(result, indent=2))
    print("=" * 70)


if __name__ == "__main__":
    main()
