"""
PSS (Protocol State System) Parser
Parses PSS language structures into JSON-serializable format.
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple


class PSSSyntaxError(Exception):
    """Raised when PSS syntax is invalid."""
    pass


class PSSParser:
    """Parser for PSS language."""

    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.col = 1

    def parse(self) -> Dict[str, Any]:
        """
        Parse PSS text and return structured JSON.
        
        Returns:
            Dict with 'success': bool, 'data': parsed_component or 'error': error_message
        """
        try:
            self._skip_whitespace()
            component = self._parse_component()
            self._skip_whitespace()
            if self.pos < len(self.text):
                raise PSSSyntaxError(f"Unexpected content at position {self.pos}")
            return {
                "success": True,
                "data": component
            }
        except PSSSyntaxError as e:
            return {
                "success": False,
                "error": str(e),
                "position": self.pos,
                "line": self.line,
                "column": self.col
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "position": self.pos
            }

    def _current_char(self) -> Optional[str]:
        """Get current character without advancing."""
        if self.pos < len(self.text):
            return self.text[self.pos]
        return None

    def _peek(self, offset: int = 1) -> Optional[str]:
        """Peek ahead at character."""
        pos = self.pos + offset
        if pos < len(self.text):
            return self.text[pos]
        return None

    def _advance(self) -> Optional[str]:
        """Consume and return current character."""
        if self.pos >= len(self.text):
            return None
        char = self.text[self.pos]
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return char

    def _skip_whitespace(self):
        """Skip whitespace and comments."""
        while self.pos < len(self.text):
            ch = self._current_char()
            if ch in ' \t\n\r':
                self._advance()
            elif ch == '/' and self._peek() == '/':
                # Single-line comment
                while self._current_char() and self._current_char() != '\n':
                    self._advance()
            elif ch == '/' and self._peek() == '*':
                # Multi-line comment
                self._advance()  # /
                self._advance()  # *
                while self.pos < len(self.text) - 1:
                    if self._current_char() == '*' and self._peek() == '/':
                        self._advance()  # *
                        self._advance()  # /
                        break
                    self._advance()
            else:
                break

    def _expect(self, expected: str) -> str:
        """Expect a specific character or string."""
        self._skip_whitespace()
        for char in expected:
            if self._current_char() != char:
                raise PSSSyntaxError(
                    f"Expected '{expected}' at line {self.line}, col {self.col}, got '{self._current_char()}'"
                )
            self._advance()
        return expected

    def _parse_identifier(self) -> str:
        """Parse an identifier (name)."""
        self._skip_whitespace()
        ident = ""
        while self.pos < len(self.text):
            ch = self._current_char()
            if ch and (ch.isalnum() or ch == '_'):
                ident += ch
                self._advance()
            else:
                break
        if not ident:
            raise PSSSyntaxError(f"Expected identifier at line {self.line}, col {self.col}")
        return ident

    def _parse_component(self) -> Dict[str, Any]:
        """Parse: component <name> { <actions> }"""
        self._expect("component")
        name = self._parse_identifier()
        self._expect("{")
        
        actions = {}
        while True:
            self._skip_whitespace()
            if self._current_char() == '}':
                break
            action = self._parse_action()
            if action["name"] in actions:
                raise PSSSyntaxError(f"Duplicate action '{action['name']}'")
            actions[action["name"]] = action
        
        self._expect("}")
        
        return {
            "type": "component",
            "name": name,
            "actions": actions
        }

    def _parse_action(self) -> Dict[str, Any]:
        """Parse: action <name> { <activity>? } ;"""
        self._expect("action")
        name = self._parse_identifier()
        self._expect("{")
        
        activity = None
        self._skip_whitespace()
        if self._current_char() != '}':
            activity = self._parse_activity()
        
        self._expect("}")
        
        # Semicolon is optional
        self._skip_whitespace()
        if self._current_char() == ';':
            self._advance()
        
        return {
            "type": "action",
            "name": name,
            "activity": activity
        }

    def _parse_activity(self) -> Dict[str, Any]:
        """Parse: activity { <do_statements> }"""
        self._expect("activity")
        self._expect("{")
        
        do_list = []
        while True:
            self._skip_whitespace()
            if self._current_char() == '}':
                break
            do_stmt = self._parse_do_statement()
            do_list.append(do_stmt)
        
        self._expect("}")
        
        return {
            "type": "activity",
            "sequence": do_list
        }

    def _parse_do_statement(self) -> Dict[str, Any]:
        """Parse: do <action_name> ;"""
        self._expect("do")
        action_name = self._parse_identifier()
        self._expect(";")
        
        return {
            "type": "do",
            "action": action_name
        }


def parse_pss(text: str) -> Dict[str, Any]:
    """
    Parse PSS code text.
    
    Args:
        text: PSS source code
        
    Returns:
        Dictionary with 'success' bool and either 'data' (parsed result) or 'error' (message)
    """
    parser = PSSParser(text)
    return parser.parse()
