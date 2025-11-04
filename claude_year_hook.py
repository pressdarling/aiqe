#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""
Claude Hook: Auto-append current year to search queries
Automatically adds the current year to search queries that lack temporal context.
"""

import json
import sys
import re
from datetime import datetime
from typing import Dict, Any, Optional


def has_year_reference(query: str) -> bool:
    """Check if query contains a year reference (2000-2099)."""
    return bool(re.search(r'20\d{2}', query))


def has_temporal_keywords(query: str) -> bool:
    """Check if query contains temporal keywords indicating recency."""
    temporal_words = [
        'latest', 'recent', 'current', 'new', 'now', 'today', 
        'this year', 'currently', 'nowadays', 'up to date',
        'modern', 'contemporary', 'updated'
    ]
    query_lower = query.lower()
    return any(word in query_lower for word in temporal_words)


def should_append_year(query: str) -> bool:
    """Determine if current year should be appended to query."""
    return not has_year_reference(query) and not has_temporal_keywords(query)


def process_hook_input() -> None:
    """Main hook processing function."""
    try:
        input_data = json.load(sys.stdin)
        tool_input = input_data.get('tool_input', {})
        query = tool_input.get('query', '')

        if not query:
            # No query to modify, pass through unchanged
            output = {
                'hookSpecificOutput': {
                    'hookEventName': 'PreToolUse',
                    'modifiedToolInput': tool_input
                }
            }
        else:
            current_year = str(datetime.now().year)

            if should_append_year(query):
                modified_query = f'{query} {current_year}'
            else:
                modified_query = query

            # Create modified tool input
            modified_tool_input = tool_input.copy()
            modified_tool_input['query'] = modified_query

            output = {
                'hookSpecificOutput': {
                    'hookEventName': 'PreToolUse',
                    'modifiedToolInput': modified_tool_input
                }
            }

        print(json.dumps(output))
        sys.exit(0)

    except Exception as e:
        # On error, pass through original input unchanged
        try:
            input_data = json.load(sys.stdin)
            output = {
                'hookSpecificOutput': {
                    'hookEventName': 'PreToolUse',
                    'modifiedToolInput': input_data.get('tool_input', {})
                }
            }
            print(json.dumps(output))
        except:
            # Fallback empty response
            print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'modifiedToolInput': {}}}))
        sys.exit(1)


if __name__ == '__main__':
    process_hook_input()
