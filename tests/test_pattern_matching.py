"""Tests for pattern matching functions - TDD RED phase"""
import pytest
from utils import has_year_reference, has_temporal_keywords


class TestHasYearReference:
    """Tests for has_year_reference function"""

    def test_detects_four_digit_year(self):
        """Should detect standard 4-digit years"""
        assert has_year_reference("python tutorials 2024") is True
        assert has_year_reference("2023 best practices") is True
        assert has_year_reference("guide for 2025") is True

    def test_detects_year_boundaries(self):
        """Should detect years at word boundaries"""
        assert has_year_reference("tutorials2024guide") is False  # No word boundary
        assert has_year_reference("tutorials 2024 guide") is True
        assert has_year_reference("2024") is True

    def test_rejects_invalid_year_patterns(self):
        """Should not match invalid year patterns"""
        assert has_year_reference("year 1999") is False  # Outside 20xx range
        assert has_year_reference("3024 future") is False  # Outside 20xx range
        assert has_year_reference("just 24") is False  # Too short
        assert has_year_reference("number 202") is False  # Too short

    def test_handles_edge_cases(self):
        """Should handle edge cases properly"""
        assert has_year_reference("") is False
        assert has_year_reference("no year here") is False
        assert has_year_reference("2000") is True  # Start of range
        assert has_year_reference("2099") is True  # End of range

    def test_multiple_years(self):
        """Should detect when multiple years present"""
        assert has_year_reference("compare 2023 vs 2024") is True

    def test_year_in_context(self):
        """Should detect years in various contexts"""
        assert has_year_reference("Python 3.12 released 2024") is True
        assert has_year_reference("version 2024.1") is True


class TestHasTemporalKeywords:
    """Tests for has_temporal_keywords function"""

    def test_detects_basic_temporal_words(self):
        """Should detect common temporal keywords"""
        assert has_temporal_keywords("latest python features") is True
        assert has_temporal_keywords("recent updates") is True
        assert has_temporal_keywords("current best practices") is True
        assert has_temporal_keywords("new features") is True

    def test_detects_all_temporal_keywords(self):
        """Should detect all defined temporal keywords"""
        keywords = [
            'latest', 'recent', 'current', 'new', 'now', 'today',
            'this year', 'currently', 'nowadays', 'up to date',
            'modern', 'contemporary', 'updated'
        ]
        for keyword in keywords:
            assert has_temporal_keywords(f"query with {keyword}") is True, f"Failed for: {keyword}"

    def test_case_insensitive(self):
        """Should be case insensitive"""
        assert has_temporal_keywords("LATEST features") is True
        assert has_temporal_keywords("Latest Features") is True
        assert has_temporal_keywords("lAtEsT features") is True

    def test_rejects_non_temporal(self):
        """Should not match queries without temporal keywords"""
        assert has_temporal_keywords("python tutorials") is False
        assert has_temporal_keywords("how to code") is False
        assert has_temporal_keywords("") is False

    def test_partial_word_matches(self):
        """Should handle partial word matches appropriately"""
        # 'new' is in 'renewable' but should still match since we use 'in'
        assert has_temporal_keywords("renewable energy") is True

    def test_multi_word_keywords(self):
        """Should detect multi-word temporal phrases"""
        assert has_temporal_keywords("this year's trends") is True
        assert has_temporal_keywords("up to date documentation") is True

    def test_multiple_keywords(self):
        """Should detect when multiple temporal keywords present"""
        assert has_temporal_keywords("latest and modern approach") is True


class TestShouldAppendYear:
    """Tests for should_append_year function"""

    def test_append_when_no_temporal_context(self):
        """Should append year when no year or temporal keywords"""
        from utils import should_append_year
        assert should_append_year("python tutorials") is True
        assert should_append_year("how to code") is True

    def test_no_append_when_year_present(self):
        """Should not append when year already present"""
        from utils import should_append_year
        assert should_append_year("python tutorials 2024") is False

    def test_no_append_when_temporal_keyword_present(self):
        """Should not append when temporal keyword present"""
        from utils import should_append_year
        assert should_append_year("latest python features") is False
        assert should_append_year("modern approach") is False
