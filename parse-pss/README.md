# PSS Parser MCP Tool

Parse PSS (Protocol State System) code into structured JSON format.

## Features

- Parses PSS component definitions with actions
- Supports action activities with do-statement sequences
- Returns detailed error messages on parse failure
- Line and column tracking for debugging
- **Full MCP (Model Context Protocol) support** - integrate with VS Code Copilot and other compatible IDEs

## Installation

```bash
cd parse-pss
pip install -r requirements.txt
```

## Usage as MCP Tool (VS Code Copilot)

### Step 1: Configure MCP in VS Code

Add the following to your VS Code settings (`.vscode/settings.json` or user settings):

```json
{
  "modelContextProtocol": {
    "tools": {
      "pss-parser": {
        "command": "python",
        "args": ["-m", "src.mcp_server"],
        "cwd": "${workspaceFolder}/parse-pss"
      }
    }
  }
}
```

Or manually in VS Code:
1. Open Command Palette (`Ctrl+Shift+P`)
2. Search for "MCP Tools"
3. Add new tool with command: `python -m src.mcp_server`
4. Set working directory: `parse-pss`

### Step 2: Start the MCP Server

Once configured, VS Code will automatically start the server when you open a chat. You can then ask Copilot:

> "Parse this PSS code for me" + [paste code]

Or in the code:

```
@pss-parser Parse this code: component pss_top { ... }
```

The tool will parse the code and return structured JSON directly in the chat.

## Usage as Python Module

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

## Run Tests

```bash
python test.py
```

## MCP Tool Definition

The MCP server exposes one tool:

**Tool Name:** `parse_pss`

**Parameters:**
- `code` (string, required): PSS source code to parse

**Returns:** JSON object with:
- `success` (boolean): Whether parsing succeeded
- `data` (object): Parsed component structure (on success)
- `error` (string): Error message with line/column info (on failure)

## PSS Grammar (Simplified)

```
component ::= "component" IDENTIFIER "{" action* "}"
action     ::= "action" IDENTIFIER "{" activity? "}" ";"?
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
- Advanced error recovery
- Performance optimizations
- Additional validation rules
