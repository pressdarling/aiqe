"""Tests for tool output formatting - TDD RED/GREEN phase"""
import pytest
from ai_query_enhancer import (
    format_for_tool,
    enhance_query,
    ToolType,
    EnhancementMode,
)


class TestFormatForTool:
    """Tests for format_for_tool function"""

    def test_claude_format(self):
        """Should format correctly for Claude"""
        result = format_for_tool(
            "enhanced query",
            ToolType.CLAUDE,
            {"tool_input": {"query": "original"}}
        )
        assert result == {
            'hookSpecificOutput': {
                'hookEventName': 'PreToolUse',
                'modifiedToolInput': {'query': 'enhanced query'}
            }
        }

    def test_claude_preserves_other_tool_input(self):
        """Should preserve other tool_input fields for Claude"""
        result = format_for_tool(
            "enhanced query",
            ToolType.CLAUDE,
            {"tool_input": {"query": "original", "other": "value"}}
        )
        assert result['hookSpecificOutput']['modifiedToolInput']['other'] == 'value'
        assert result['hookSpecificOutput']['modifiedToolInput']['query'] == 'enhanced query'

    def test_codex_format(self):
        """Should format correctly for Codex"""
        result = format_for_tool(
            "enhanced query",
            ToolType.CODEX,
            {"model": "gpt-4o", "max_tokens": 500}
        )
        assert result == {
            'prompt': 'enhanced query',
            'model': 'gpt-4o',
            'max_tokens': 500
        }

    def test_codex_default_values(self):
        """Should use default values for Codex when not provided"""
        result = format_for_tool("enhanced query", ToolType.CODEX, {})
        assert result['model'] == 'gpt-4'
        assert result['max_tokens'] == 1000

    def test_gemini_format(self):
        """Should format correctly for Gemini"""
        result = format_for_tool(
            "enhanced query",
            ToolType.GEMINI,
            {"generationConfig": {"temperature": 0.7}}
        )
        assert result == {
            'contents': [{'parts': [{'text': 'enhanced query'}]}],
            'generationConfig': {'temperature': 0.7}
        }

    def test_gemini_default_config(self):
        """Should use empty generationConfig when not provided"""
        result = format_for_tool("enhanced query", ToolType.GEMINI, {})
        assert result['generationConfig'] == {}

    def test_cursor_generic_format(self):
        """Should use generic format for Cursor"""
        original = {"some": "data"}
        result = format_for_tool("enhanced query", ToolType.CURSOR, original)
        assert result == {
            'query': 'enhanced query',
            'original': original
        }

    def test_copilot_generic_format(self):
        """Should use generic format for Copilot"""
        original = {"some": "data"}
        result = format_for_tool("enhanced query", ToolType.COPILOT, original)
        assert result == {
            'query': 'enhanced query',
            'original': original
        }

    def test_empty_original_data(self):
        """Should handle empty original data"""
        result = format_for_tool("query", ToolType.CLAUDE, {})
        assert result['hookSpecificOutput']['modifiedToolInput'] == {'query': 'query'}


class TestEnhanceQuery:
    """Tests for enhance_query dispatcher function"""

    def test_year_append_mode(self):
        """Should apply year-append enhancement"""
        from datetime import datetime
        current_year = str(datetime.now().year)
        result = enhance_query("python tutorials", EnhancementMode.YEAR_APPEND)
        assert result == f"python tutorials {current_year}"

    def test_context_inject_mode(self):
        """Should apply context-inject enhancement"""
        result = enhance_query(
            "how to handle errors",
            EnhancementMode.CONTEXT_INJECT,
            context="TypeScript project"
        )
        assert result == "In the context of TypeScript project: how to handle errors"

    def test_context_inject_without_context(self):
        """Should return original query if context not provided"""
        result = enhance_query("query", EnhancementMode.CONTEXT_INJECT)
        assert result == "query"

    def test_technical_focus_mode(self):
        """Should apply tech-focus enhancement"""
        result = enhance_query("error handling", EnhancementMode.TECHNICAL_FOCUS)
        assert "modern development practices" in result

    def test_australian_context_mode(self):
        """Should apply au-context enhancement"""
        result = enhance_query("legal requirements", EnhancementMode.AUSTRALIAN_CONTEXT)
        assert "(Australian context)" in result

    def test_unknown_mode_returns_original(self):
        """Should return original query for unhandled cases"""
        # This tests the fallback behavior
        result = enhance_query("query", EnhancementMode.CONTEXT_INJECT)
        assert result == "query"


class TestToolTypeEnum:
    """Tests for ToolType enum"""

    def test_all_tools_defined(self):
        """Should have all expected tool types"""
        assert ToolType.CLAUDE.value == "claude"
        assert ToolType.CODEX.value == "codex"
        assert ToolType.GEMINI.value == "gemini"
        assert ToolType.CURSOR.value == "cursor"
        assert ToolType.COPILOT.value == "copilot"


class TestEnhancementModeEnum:
    """Tests for EnhancementMode enum"""

    def test_all_modes_defined(self):
        """Should have all expected enhancement modes"""
        assert EnhancementMode.YEAR_APPEND.value == "year-append"
        assert EnhancementMode.CONTEXT_INJECT.value == "context-inject"
        assert EnhancementMode.TECHNICAL_FOCUS.value == "tech-focus"
        assert EnhancementMode.AUSTRALIAN_CONTEXT.value == "au-context"
