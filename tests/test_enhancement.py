"""Tests for enhancement functions - TDD RED/GREEN phase"""
import pytest
from datetime import datetime
from unittest.mock import patch
from utils import (
    enhance_with_year,
    enhance_with_context,
    enhance_with_technical_focus,
    enhance_with_australian_context,
)


class TestEnhanceWithYear:
    """Tests for enhance_with_year function"""

    def test_appends_year_to_plain_query(self):
        """Should append current year to queries without temporal context"""
        current_year = str(datetime.now().year)
        result = enhance_with_year("python tutorials")
        assert result == f"python tutorials {current_year}"

    def test_preserves_query_with_year(self):
        """Should not modify queries that already have a year"""
        query = "python tutorials 2024"
        result = enhance_with_year(query)
        assert result == query

    def test_preserves_query_with_temporal_keyword(self):
        """Should not modify queries with temporal keywords"""
        query = "latest python features"
        result = enhance_with_year(query)
        assert result == query

    def test_handles_empty_string(self):
        """Should handle empty string input"""
        current_year = str(datetime.now().year)
        result = enhance_with_year("")
        assert result == f" {current_year}"

    @patch('utils.datetime')
    def test_uses_current_year(self, mock_datetime):
        """Should use the actual current year"""
        mock_datetime.now.return_value.year = 2030
        result = enhance_with_year("python tutorials")
        assert "2030" in result


class TestEnhanceWithContext:
    """Tests for enhance_with_context function"""

    def test_injects_context(self):
        """Should inject context into query"""
        result = enhance_with_context("how to handle errors", "TypeScript project")
        assert result == "In the context of TypeScript project: how to handle errors"

    def test_handles_empty_query(self):
        """Should handle empty query"""
        result = enhance_with_context("", "some context")
        assert result == "In the context of some context: "

    def test_handles_empty_context(self):
        """Should handle empty context"""
        result = enhance_with_context("query", "")
        assert result == "In the context of : query"

    def test_preserves_special_characters(self):
        """Should preserve special characters in both query and context"""
        result = enhance_with_context("what's the best way?", "React & TypeScript")
        assert result == "In the context of React & TypeScript: what's the best way?"

    def test_handles_multiline_query(self):
        """Should handle multiline queries"""
        query = "line1\nline2"
        result = enhance_with_context(query, "context")
        assert "line1\nline2" in result


class TestEnhanceWithTechnicalFocus:
    """Tests for enhance_with_technical_focus function"""

    def test_adds_tech_focus_to_plain_query(self):
        """Should add tech focus to queries without tech keywords"""
        result = enhance_with_technical_focus("error handling")
        assert "modern development practices" in result
        assert "TypeScript" in result

    def test_preserves_query_with_best_practices(self):
        """Should not modify queries with 'best practices'"""
        query = "Python best practices"
        result = enhance_with_technical_focus(query)
        assert result == query

    def test_preserves_query_with_production_ready(self):
        """Should not modify queries with 'production ready'"""
        query = "make it production ready"
        result = enhance_with_technical_focus(query)
        assert result == query

    def test_preserves_query_with_typescript(self):
        """Should not modify queries already mentioning TypeScript"""
        query = "TypeScript generics"
        result = enhance_with_technical_focus(query)
        assert result == query

    def test_preserves_query_with_modern_approach(self):
        """Should not modify queries with 'modern approach'"""
        query = "what is the modern approach"
        result = enhance_with_technical_focus(query)
        assert result == query

    def test_case_insensitive_detection(self):
        """Should detect keywords case-insensitively"""
        query = "BEST PRACTICES for coding"
        result = enhance_with_technical_focus(query)
        assert result == query

    def test_handles_empty_string(self):
        """Should handle empty string"""
        result = enhance_with_technical_focus("")
        assert "modern development practices" in result


class TestEnhanceWithAustralianContext:
    """Tests for enhance_with_australian_context function"""

    def test_adds_au_context_for_legal(self):
        """Should add AU context for legal queries"""
        result = enhance_with_australian_context("legal requirements for contracts")
        assert result == "legal requirements for contracts (Australian context)"

    def test_adds_au_context_for_tax(self):
        """Should add AU context for tax queries"""
        result = enhance_with_australian_context("tax deductions")
        assert "(Australian context)" in result

    def test_adds_au_context_for_regulation(self):
        """Should add AU context for regulation queries"""
        result = enhance_with_australian_context("data regulation")
        assert "(Australian context)" in result

    def test_adds_au_context_for_compliance(self):
        """Should add AU context for compliance queries"""
        result = enhance_with_australian_context("compliance requirements")
        assert "(Australian context)" in result

    def test_adds_au_context_for_business(self):
        """Should add AU context for business queries"""
        result = enhance_with_australian_context("business registration")
        assert "(Australian context)" in result

    def test_adds_au_context_for_government(self):
        """Should add AU context for government queries"""
        result = enhance_with_australian_context("government grants")
        assert "(Australian context)" in result

    def test_preserves_non_au_queries(self):
        """Should not modify queries without AU indicators"""
        query = "python tutorials"
        result = enhance_with_australian_context(query)
        assert result == query

    def test_case_insensitive_detection(self):
        """Should detect indicators case-insensitively"""
        result = enhance_with_australian_context("LEGAL advice")
        assert "(Australian context)" in result

    def test_handles_empty_string(self):
        """Should handle empty string"""
        result = enhance_with_australian_context("")
        assert result == ""
