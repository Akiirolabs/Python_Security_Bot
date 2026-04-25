from __future__ import annotations

from collections.abc import Mapping, Sequence

from .models import EnrichmentResult, Severity, Verdict

DEFAULT_RISK_WEIGHTS: dict[Verdict, int] = {
    "benign": 0,
    "unknown": 20,
    "malicious": 80,
}

BAD_VERDICTS: set[Verdict] = {"malicious"}


def compute_score(
    enrichment_results: Sequence[EnrichmentResult],
    risk_weights: Mapping[Verdict, int] | None = None,
) -> int:
    """Compute a case risk score from enrichment results.

    The highest vendor verdict sets the base score. Additional bad verdicts add
    a small capped bonus so multiple malicious indicators push the case upward
    without exceeding the 0-100 score range.
    """
    weights = risk_weights or DEFAULT_RISK_WEIGHTS
    base = 0
    bad_count = 0

    for enrichment in enrichment_results:
        base = max(base, _clamp_score(weights.get(enrichment.verdict, 0)))
        if enrichment.verdict in BAD_VERDICTS:
            bad_count += 1

    bonus = min(20, bad_count * 5)
    return _clamp_score(base + bonus)


def severity_from_score(score: int) -> Severity:
    score = _clamp_score(score)
    if score >= 85:
        return "critical"
    if score >= 60:
        return "high"
    if score >= 30:
        return "medium"
    return "low"


def _clamp_score(score: int) -> int:
    return max(0, min(100, int(score)))
