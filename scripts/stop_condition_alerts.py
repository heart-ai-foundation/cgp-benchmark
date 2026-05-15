"""Helpers for detecting live stop-condition events in agent transcripts."""

from __future__ import annotations

import re


TRUE_STOP_PATTERNS = (
    re.compile(r"\bstopping per\b", re.IGNORECASE),
    re.compile(r"\bstop[- ]condition(?:\s+\w+){0,3}\s+triggered\b", re.IGNORECASE),
    re.compile(r"\bconflict detected\b", re.IGNORECASE),
    re.compile(r"\bload-bearing disagreement\b", re.IGNORECASE),
    re.compile(r"\bprotocol conflict\b", re.IGNORECASE),
)

NEGATED_STOP_PATTERNS = (
    re.compile(r"\bstop[- ]condition(?:\s+\w+){0,3}\s+not triggered\b", re.IGNORECASE),
    re.compile(r"\bno stop[- ]condition(?:\s+\w+){0,3}\s+triggered\b", re.IGNORECASE),
)


def is_stop_condition_alert(fragment: str) -> bool:
    """Return True only for agent output that appears to report an actual stop."""
    text = fragment.strip()
    if not text:
        return False
    lowered = text.lower()

    if any(pattern.search(text) for pattern in NEGATED_STOP_PATTERNS):
        return False

    # Avoid alerting on quoted protocol/scaffold content that defines the rule.
    if '"stop_condition"' in lowered or "'stop_condition'" in lowered:
        return False
    if "stop and report" in lowered and "stopping per" not in lowered:
        return False
    if "if the active protocol" in lowered:
        return False

    return any(pattern.search(text) for pattern in TRUE_STOP_PATTERNS)
