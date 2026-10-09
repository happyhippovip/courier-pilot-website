"""Secondary pages must not present concept goals as finished proof."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def test_use_cases_are_concept_not_proven_catalog():
    text = _read("use-cases.html")
    assert "Proven Use Cases" not in text
    assert "Real-World Operations" not in text
    assert "deliver immediate value" not in text
    assert "Concept use cases" in text
    assert "PR #361" in text
    assert 'style="margin-top:' not in text


def test_company_lanes_are_roadmap_not_absolute_guarantees():
    text = _read("company.html")
    assert "zero new test exclusions" not in text
    assert "end-to-end failover tests" not in text
    assert "Technical lane roadmap" in text
    assert "Gründung in Vorbereitung" in text
    assert 'style="margin-top:' not in text
