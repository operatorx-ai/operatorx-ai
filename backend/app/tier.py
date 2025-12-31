from __future__ import annotations

from typing import Literal

Tier = Literal["personal", "business", "government"]

DEFAULT_TIER: Tier = "personal"
ALLOWED_TIERS = {"personal", "business", "government"}


def normalize_tier(value: str | None) -> Tier:
    """
    Normalize and validate the incoming tier.
    """
    if not value:
        return DEFAULT_TIER

    v = value.strip().lower()
    if v not in ALLOWED_TIERS:
        return DEFAULT_TIER

    return v  # type: ignore[return-value]
