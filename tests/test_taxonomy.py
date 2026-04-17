"""Tests for src/data/skills_taxonomy.py."""

import pytest


def test_import() -> None:
    """Taxonomy module imports without error."""
    import src.data.skills_taxonomy  # noqa: F401


def test_get_categories_not_empty() -> None:
    """get_categories() returns a list with at least 10 items."""
    from src.data.skills_taxonomy import get_categories

    categories = get_categories()
    assert isinstance(categories, list)
    assert len(categories) >= 10


def test_get_all_keywords_not_empty() -> None:
    """get_all_keywords() returns a dict with at least 150 entries."""
    from src.data.skills_taxonomy import get_all_keywords

    keywords = get_all_keywords()
    assert isinstance(keywords, dict)
    assert len(keywords) >= 150


def test_no_duplicate_keywords() -> None:
    """Calling get_all_keywords() does not raise ValueError (no duplicate aliases)."""
    from src.data.skills_taxonomy import get_all_keywords

    try:
        get_all_keywords()
    except ValueError as exc:
        pytest.fail(f"Duplicate keyword found in taxonomy: {exc}")


def test_all_keywords_lowercase() -> None:
    """Every key in get_all_keywords() is lowercase."""
    from src.data.skills_taxonomy import get_all_keywords

    keywords = get_all_keywords()
    non_lowercase = [k for k in keywords if k != k.lower()]
    assert non_lowercase == [], f"Non-lowercase keyword aliases found: {non_lowercase}"


def test_canonical_skill_in_category() -> None:
    """Spot-check: 'Python' is a canonical skill under 'Programming Languages'."""
    from src.data.skills_taxonomy import SKILLS_TAXONOMY

    assert "Programming Languages" in SKILLS_TAXONOMY
    assert "Python" in SKILLS_TAXONOMY["Programming Languages"]


def test_ai_genai_keywords_present() -> None:
    """Spot-check: 'llm', 'rag', and 'prompt engineering' appear as keyword aliases."""
    from src.data.skills_taxonomy import get_all_keywords

    keywords = get_all_keywords()
    assert "llm" in keywords, "'llm' not found in keyword aliases"
    assert "rag" in keywords, "'rag' not found in keyword aliases"
    assert "prompt engineering" in keywords, "'prompt engineering' not found in keyword aliases"
