#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = ["click", "pydantic"]
# ///
"""
AI Tool Query Enhancer
A flexible script for enhancing queries across different AI coding tools.

Usage examples:
- python ai_query_enhancer.py --tool claude --mode year-append "search for python tutorials"
- python ai_query_enhancer.py --tool codex --mode context-inject --context "TypeScript project" "how to handle errors"
- python ai_query_enhancer.py --tool gemini --mode stdin-json < input.json
"""

import json
import sys
import click
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum

from utils import (
    enhance_with_year,
    enhance_with_context,
    enhance_with_technical_focus,
    enhance_with_australian_context,
)


class ToolType(str, Enum):
    CLAUDE = "claude"
    CODEX = "codex"
    GEMINI = "gemini"
    CURSOR = "cursor"
    COPILOT = "copilot"


class EnhancementMode(str, Enum):
    YEAR_APPEND = "year-append"
    CONTEXT_INJECT = "context-inject"
    TECHNICAL_FOCUS = "tech-focus"
    AUSTRALIAN_CONTEXT = "au-context"


def enhance_query(query: str, mode: EnhancementMode, context: Optional[str] = None) -> str:
    """Apply the specified enhancement to the query."""
    if mode == EnhancementMode.YEAR_APPEND:
        return enhance_with_year(query)
    elif mode == EnhancementMode.CONTEXT_INJECT and context:
        return enhance_with_context(query, context)
    elif mode == EnhancementMode.TECHNICAL_FOCUS:
        return enhance_with_technical_focus(query)
    elif mode == EnhancementMode.AUSTRALIAN_CONTEXT:
        return enhance_with_australian_context(query)
    return query


def format_for_tool(enhanced_query: str, tool: ToolType, original_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format the enhanced query for the specific tool."""
    if tool == ToolType.CLAUDE:
        # Claude hook format
        return {
            'hookSpecificOutput': {
                'hookEventName': 'PreToolUse',
                'modifiedToolInput': {**original_data.get('tool_input', {}), 'query': enhanced_query}
            }
        }
    elif tool == ToolType.CODEX:
        # OpenAI Codex CLI format
        return {
            'prompt': enhanced_query,
            'model': original_data.get('model', 'gpt-4'),
            'max_tokens': original_data.get('max_tokens', 1000)
        }
    elif tool == ToolType.GEMINI:
        # Gemini CLI format
        return {
            'contents': [{'parts': [{'text': enhanced_query}]}],
            'generationConfig': original_data.get('generationConfig', {})
        }
    else:
        # Generic format
        return {'query': enhanced_query, 'original': original_data}


@click.command()
@click.option('--tool', type=click.Choice([t.value for t in ToolType]), default='claude', 
              help='Target AI tool')
@click.option('--mode', type=click.Choice([m.value for m in EnhancementMode]), 
              default='year-append', help='Enhancement mode')
@click.option('--context', help='Additional context for context-inject mode')
@click.option('--stdin-json', is_flag=True, help='Read JSON input from stdin')
@click.argument('query', required=False)
def main(tool: str, mode: str, context: Optional[str], stdin_json: bool, query: Optional[str]):
    """Enhance AI tool queries with contextual information."""

    tool_enum = ToolType(tool)
    mode_enum = EnhancementMode(mode)

    if stdin_json:
        # Read from stdin (Claude hook mode)
        try:
            input_data = json.load(sys.stdin)
            original_query = input_data.get('tool_input', {}).get('query', '')
        except json.JSONDecodeError:
            click.echo("Error: Invalid JSON input", err=True)
            sys.exit(1)
    elif query:
        # Direct query mode
        input_data = {}
        original_query = query
    else:
        click.echo("Error: Provide either --stdin-json or a query argument", err=True)
        sys.exit(1)

    if not original_query:
        click.echo("Error: No query found", err=True)
        sys.exit(1)

    # Enhance the query
    enhanced_query = enhance_query(original_query, mode_enum, context)

    # Format for target tool
    output = format_for_tool(enhanced_query, tool_enum, input_data)

    # Output result
    if stdin_json and tool_enum == ToolType.CLAUDE:
        # Claude hook output to stdout
        print(json.dumps(output))
    else:
        # Pretty print for other modes
        click.echo(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
