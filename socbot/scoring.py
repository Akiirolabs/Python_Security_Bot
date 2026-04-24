from __future__ import annotations

from typing import dict, List

from .models import EnrichmentResult, severity

def compute_score(enrichment_results: List[EnrichmentResult], risk_weights: dict[Severity, int]) -> int:
    base = 0
    bad count = 0
    
    for enrichment in enrichments:
        base = max(base, int(weights.get(enrichment.verdict, 0)))
        if enrichment.verdict in ("malicious", "suspicious"):
            bad_count += 1
    
    bonus = min(20, bad_count * 5)
    return min(100, base + bonus)


def severrity_from_score(score: int) -> Severity:
    if score >= 85:
        return "critical"
    if score >= 60:
        return "high"
    if score >= 30:
        return "medium"
    return "low"

def seve