#!/usr/bin/env python3
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
import re
import click
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum


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


def has_year_reference(query: str) -> bool:
    """Check if query contains a year reference."""
    return bool(re.search(r'\b20\d{2}\b', query))


def has_temporal_keywords(query: str) -> bool:
    """Check if query contains temporal keywords."""
    temporal_words = [
        'latest', 'recent', 'current', 'new', 'now', 'today', 
        'this year', 'currently', 'nowadays', 'up to date',
        'modern', 'contemporary', 'updated', 'cutting edge'
    ]
    return any(word in query.lower() for word in temporal_words)


def enhance_with_year(query: str) -> str:
    """Add current year if query lacks temporal context."""
    if not has_year_reference(query) and not has_temporal_keywords(query):
        current_year = str(datetime.now().year)
        return f'{query} {current_year}'
    return query


def enhance_with_context(query: str, context: str) -> str:
    """Inject contextual information into query."""
    return f"In the context of {context}: {query}"


def enhance_with_technical_focus(query: str) -> str:
    """Add technical development context."""
    tech_keywords = ['best practices', 'production ready', 'TypeScript', 'modern approach']
    if not any(keyword.lower() in query.lower() for keyword in tech_keywords):
        return f"{query} (focus on modern development practices and TypeScript where applicable)"
    return query


def enhance_with_australian_context(query: str) -> str:
    """Add Australian context where relevant."""
    au_indicators = ['legal', 'tax', 'regulation', 'compliance', 'business', 'government']
    if any(indicator in query.lower() for indicator in au_indicators):
        return f"{query} (Australian context)"
    return query


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

if __name__ == "__main__":
    main()
