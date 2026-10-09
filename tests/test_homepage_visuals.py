"""Homepage visual integration: og-cover hero, run states, Konzept thumbs, no Stripe."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
KONZEPT = (ROOT / "konzept.html").read_text(encoding="utf-8")


def test_hero_uses_og_cover_with_dimensions_and_alt():
    assert 'src="/og-cover.png"' in INDEX
    assert 'alt="Courier Symphony' in INDEX
    assert 'width="1200"' in INDEX and 'height="630"' in INDEX
    assert 'fetchpriority="high"' in INDEX


def test_run_states_are_present():
    for state in ("Working", "Waiting", "Needs you", "Unknown", "Verified"):
        assert state in INDEX


def test_konzept_thumbs_lazy_with_alt():
    for name in ("landing-thumb.webp", "workflows-thumb.webp", "so-funktionierts-thumb.webp"):
        assert f"/assets/konzept/{name}" in INDEX
    assert INDEX.count('loading="lazy"') >= 3


def test_homepage_visuals_use_responsive_srcset_and_sizes():
    """Thumbs for narrow viewports; full WebP when the 3-col grid has room."""
    for stem in ("landing", "workflows", "so-funktionierts"):
        assert f"/assets/konzept/{stem}-thumb.webp" in INDEX
        assert f"/assets/konzept/{stem}.webp" in INDEX
        assert f'srcset="/assets/konzept/{stem}-thumb.webp' in INDEX
    assert 'sizes="(min-width: 720px) 30vw, 92vw"' in INDEX
    assert INDEX.count('sizes="(min-width: 720px) 30vw, 92vw"') >= 3


def test_konzept_lightbox_width_matches_real_assets():
    """Lightbox must not claim width=1600 when files are smaller (layout/CLS honesty)."""
    assert 'width="1600"' not in KONZEPT
    # Spot-check measured originals (Pillow-free; sizes from on-disk assets).
    assert re.search(
        r'src="/assets/konzept/landing\.webp"[^>]*width="1170"[^>]*height="662"',
        KONZEPT,
    )
    assert re.search(
        r'src="/assets/konzept/hub-launch\.webp"[^>]*width="1476"[^>]*height="1074"',
        KONZEPT,
    )
    assert re.search(
        r'src="/assets/konzept/so-funktionierts\.webp"[^>]*width="1170"[^>]*height="1462"',
        KONZEPT,
    )

def test_no_stripe_or_paid_ctas_on_homepage():
    banned = ("buy.stripe.com", "Sofort bezahlen", "5 €", "79 €", "Production-Grade")
    for token in banned:
        assert token not in INDEX


def test_nav_reaches_visuals_and_early_access():
    assert 'href="#visuals"' in INDEX
    assert 'href="#early-access"' in INDEX
