"""Tests for Claude hook JSON I/O - TDD RED/GREEN phase"""
import pytest
import json
import sys
from io import StringIO
from unittest.mock import patch
from datetime import datetime


class TestClaudeHookProcessing:
    """Tests for process_hook_input function in claude_year_hook"""

    def test_appends_year_to_plain_query(self):
        """Should append year to query without temporal context"""
        from claude_year_hook import process_hook_input

        input_data = {
            "tool_input": {"query": "python tutorials"}
        }
        current_year = str(datetime.now().year)

        with patch('sys.stdin', StringIO(json.dumps(input_data))):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with pytest.raises(SystemExit) as exc_info:
                    process_hook_input()

                assert exc_info.value.code == 0
                result = json.loads(mock_stdout.getvalue())
                assert result['hookSpecificOutput']['modifiedToolInput']['query'] == f"python tutorials {current_year}"

    def test_preserves_query_with_year(self):
        """Should not modify query that already has a year"""
        from claude_year_hook import process_hook_input

        input_data = {
            "tool_input": {"query": "python tutorials 2024"}
        }

        with patch('sys.stdin', StringIO(json.dumps(input_data))):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with pytest.raises(SystemExit) as exc_info:
                    process_hook_input()

                assert exc_info.value.code == 0
                result = json.loads(mock_stdout.getvalue())
                assert result['hookSpecificOutput']['modifiedToolInput']['query'] == "python tutorials 2024"

    def test_preserves_query_with_temporal_keyword(self):
        """Should not modify query with temporal keywords"""
        from claude_year_hook import process_hook_input

        input_data = {
            "tool_input": {"query": "latest python features"}
        }

        with patch('sys.stdin', StringIO(json.dumps(input_data))):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with pytest.raises(SystemExit) as exc_info:
                    process_hook_input()

                assert exc_info.value.code == 0
                result = json.loads(mock_stdout.getvalue())
                assert result['hookSpecificOutput']['modifiedToolInput']['query'] == "latest python features"

    def test_handles_empty_query(self):
        """Should handle empty query by passing through unchanged"""
        from claude_year_hook import process_hook_input

        input_data = {
            "tool_input": {"query": ""}
        }

        with patch('sys.stdin', StringIO(json.dumps(input_data))):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with pytest.raises(SystemExit) as exc_info:
                    process_hook_input()

                assert exc_info.value.code == 0
                result = json.loads(mock_stdout.getvalue())
                # Empty query triggers no-query path
                assert 'hookSpecificOutput' in result

    def test_handles_missing_query_field(self):
        """Should handle missing query field gracefully"""
        from claude_year_hook import process_hook_input

        input_data = {
            "tool_input": {"other": "data"}
        }

        with patch('sys.stdin', StringIO(json.dumps(input_data))):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with pytest.raises(SystemExit) as exc_info:
                    process_hook_input()

                assert exc_info.value.code == 0
                result = json.loads(mock_stdout.getvalue())
                assert 'hookSpecificOutput' in result

    def test_handles_missing_tool_input(self):
        """Should handle missing tool_input field"""
        from claude_year_hook import process_hook_input

        input_data = {"other": "data"}

        with patch('sys.stdin', StringIO(json.dumps(input_data))):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with pytest.raises(SystemExit) as exc_info:
                    process_hook_input()

                assert exc_info.value.code == 0
                result = json.loads(mock_stdout.getvalue())
                assert 'hookSpecificOutput' in result

    def test_preserves_other_tool_input_fields(self):
        """Should preserve other fields in tool_input"""
        from claude_year_hook import process_hook_input

        input_data = {
            "tool_input": {
                "query": "python tutorials",
                "other_field": "value",
                "number": 42
            }
        }

        with patch('sys.stdin', StringIO(json.dumps(input_data))):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with pytest.raises(SystemExit) as exc_info:
                    process_hook_input()

                assert exc_info.value.code == 0
                result = json.loads(mock_stdout.getvalue())
                modified = result['hookSpecificOutput']['modifiedToolInput']
                assert modified['other_field'] == 'value'
                assert modified['number'] == 42

    def test_outputs_correct_hook_event_name(self):
        """Should output correct hookEventName"""
        from claude_year_hook import process_hook_input

        input_data = {"tool_input": {"query": "test"}}

        with patch('sys.stdin', StringIO(json.dumps(input_data))):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with pytest.raises(SystemExit):
                    process_hook_input()

                result = json.loads(mock_stdout.getvalue())
                assert result['hookSpecificOutput']['hookEventName'] == 'PreToolUse'


class TestClaudeHookErrorHandling:
    """Tests for error handling in claude_year_hook"""

    def test_handles_invalid_json(self):
        """Should handle malformed JSON input gracefully"""
        from claude_year_hook import process_hook_input

        with patch('sys.stdin', StringIO("not valid json")):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with pytest.raises(SystemExit) as exc_info:
                    process_hook_input()

                # Should exit with error code
                assert exc_info.value.code == 1

    def test_handles_empty_input(self):
        """Should handle empty stdin"""
        from claude_year_hook import process_hook_input

        with patch('sys.stdin', StringIO("")):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with pytest.raises(SystemExit) as exc_info:
                    process_hook_input()

                assert exc_info.value.code == 1


class TestClaudeHookHelperFunctions:
    """Tests for helper functions used by claude_year_hook (now in utils)"""

    def test_has_year_reference(self):
        """Should detect year references"""
        from utils import has_year_reference

        assert has_year_reference("test 2024") is True
        assert has_year_reference("no year") is False

    def test_has_temporal_keywords(self):
        """Should detect temporal keywords"""
        from utils import has_temporal_keywords

        assert has_temporal_keywords("latest features") is True
        assert has_temporal_keywords("python basics") is False

    def test_should_append_year(self):
        """Should determine if year should be appended"""
        from utils import should_append_year

        assert should_append_year("python tutorials") is True
        assert should_append_year("python 2024") is False
        assert should_append_year("latest python") is False
