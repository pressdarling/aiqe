"""
Shared utilities for AI Query Enhancer.
Contains common pattern matching and enhancement functions.
"""

import re
from datetime import datetime
from typing import Optional


def has_year_reference(query: str) -> bool:
    """
    Check if query contains a year reference (2000-2099).

    Uses word boundaries to avoid matching years embedded in other numbers.
    """
    return bool(re.search(r'\b20\d{2}\b', query))


def has_temporal_keywords(query: str) -> bool:
    """
    Check if query contains temporal keywords indicating recency.

    Returns True if any temporal keyword is found (case-insensitive).
    """
    temporal_words = [
        'latest', 'recent', 'current', 'new', 'now', 'today',
        'this year', 'currently', 'nowadays', 'up to date',
        'modern', 'contemporary', 'updated', 'cutting edge'
    ]
    query_lower = query.lower()
    return any(word in query_lower for word in temporal_words)


def should_append_year(query: str) -> bool:
    """
    Determine if current year should be appended to query.

    Returns True if query has no year reference and no temporal keywords.
    """
    return not has_year_reference(query) and not has_temporal_keywords(query)


def enhance_with_year(query: str) -> str:
    """
    Add current year if query lacks temporal context.

    Returns the original query with year appended, or unchanged if
    temporal context already exists.
    """
    if should_append_year(query):
        current_year = str(datetime.now().year)
        return f'{query} {current_year}'
    return query


def enhance_with_context(query: str, context: str) -> str:
    """
    Inject contextual information into query.

    Args:
        query: The original query
        context: Additional context to inject

    Returns:
        Query with context prepended
    """
    return f"In the context of {context}: {query}"


def enhance_with_technical_focus(query: str) -> str:
    """
    Add technical development context to query.

    Returns query with tech focus appended if no tech keywords present.
    """
    tech_keywords = ['best practices', 'production ready', 'typescript', 'modern approach']
    if not any(keyword in query.lower() for keyword in tech_keywords):
        return f"{query} (focus on modern development practices and TypeScript where applicable)"
    return query


def enhance_with_australian_context(query: str) -> str:
    """
    Add Australian context where relevant.

    Appends Australian context indicator for queries containing
    legal, tax, regulatory, or business keywords.
    """
    au_indicators = ['legal', 'tax', 'regulation', 'compliance', 'business', 'government']
    if any(indicator in query.lower() for indicator in au_indicators):
        return f"{query} (Australian context)"
    return query
