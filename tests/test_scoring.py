from socbot.models import IOC, EnrichmentResult
from socbot.scoring import compute_score, severity_from_score


def test_scoring_and_severity():
    ioc = IOC(type="domain", value="a.com", normalized="a.com")

    enrichments = [
        EnrichmentResult(vendor="x", ioc=ioc, verdict="unknown", confidence=40, details={}),
        EnrichmentResult(vendor="x", ioc=ioc, verdict="suspicious", confidence=60, details={}),
    ]

    weights = {
        "malicious": 70,
        "suspicious": 30,
        "unknown": 10,
        "clean": 0,
    }

    score = compute_score(enrichments, weights)
    assert 30 <= score <= 100
    assert severity_from_score(score) in ("Medium", "High", "Critical")
