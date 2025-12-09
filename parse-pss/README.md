# PSS Parser MCP Tool

Parse PSS (Protocol State System) code into structured JSON format.

## Features

- Parses PSS component definitions with actions
- Supports action activities with do-statement sequences
- Returns detailed error messages on parse failure
- Line and column tracking for debugging

## Installation

```bash
cd parse-pss
pip install -r requirements.txt
```

## Usage

### As a Python Module

```python
from src.pss_parser import parse_pss

code = """component pss_top {
    action A {};
    action B {};
}"""

result = parse_pss(code)
if result["success"]:
    print(result["data"])
else:
    print(f"Error: {result['error']}")
```

### Run Tests

```bash
python test.py
```

## MCP Tool Integration

The parser is designed to work as an MCP (Model Context Protocol) tool that can be integrated with VS Code Copilot or other compatible IDEs.

## PSS Grammar (Simplified)

```
component ::= "component" IDENTIFIER "{" action* "}"
action     ::= "action" IDENTIFIER "{" activity? "}" ";"
activity   ::= "activity" "{" do_statement* "}"
do_statement ::= "do" IDENTIFIER ";"
```

## Output Format

**Success:**
```json
{
  "success": true,
  "data": {
    "type": "component",
    "name": "pss_top",
    "actions": {
      "A": {"type": "action", "name": "A", "activity": null},
      "C": {
        "type": "action",
        "name": "C",
        "activity": {
          "type": "activity",
          "sequence": [
            {"type": "do", "action": "A"},
            {"type": "do", "action": "B"}
          ]
        }
      }
    }
  }
}
```

**Failure:**
```json
{
  "success": false,
  "error": "Expected identifier at line 1, col 15",
  "position": 14,
  "line": 1,
  "column": 15
}
```

## Future Enhancements

- Support for more complex PSS constructs (constraints, randomization, etc.)
- Integration with official MCP SDK
- Advanced error recovery
- Performance optimizations
