"""Homepage visual integration: og-cover hero, run states, Konzept thumbs, no Stripe."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")


def test_hero_uses_og_cover_with_dimensions_and_alt():
    assert 'src="/og-cover.png"' in INDEX
    assert 'alt="Courier Symphony' in INDEX
    assert 'width="1200"' in INDEX and 'height="630"' in INDEX
    assert 'fetchpriority="high"' in INDEX


def test_run_states_are_present():
    for state in ("Working", "Waiting", "Blocked", "Unknown", "Verified"):
        assert state in INDEX


def test_konzept_thumbs_lazy_with_alt():
    for name in ("landing-thumb.webp", "workflows-thumb.webp", "so-funktionierts-thumb.webp"):
        assert f"/assets/konzept/{name}" in INDEX
    assert INDEX.count('loading="lazy"') >= 3


def test_no_stripe_or_paid_ctas_on_homepage():
    banned = ("buy.stripe.com", "Sofort bezahlen", "5 €", "79 €", "Production-Grade")
    for token in banned:
        assert token not in INDEX


def test_nav_reaches_visuals_and_early_access():
    assert 'href="#visuals"' in INDEX
    assert 'href="#early-access"' in INDEX
