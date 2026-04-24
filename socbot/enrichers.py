from __future__ import annotations

import hashlib
from typing import List

from .cache import DiskTTLCache
from .models import EnrichmentResult, IOC, Verdict


class MockEnricher:
    def __init__(self, cache: DiskTTLCache):
        self.cache = cache
        self.vendor = "mock-ti"

    def enrich_ioc(self, ioc: IOC) -> EnrichmentResult:
        cache_key = f"{self.vendor}:{ioc.type}:{ioc.normalized}"
        cached = self.cache.get(cache_key)
        if cached:
            return EnrichmentResult(**cached)
        
        digest = hashlib.sha256(ioc.normalized.encode()).hexdigest()
        bucket = int(digest[:2], 16) % 4

        verdict_map: dict[int, tuple[Verdict, int]] = {
            0: ("benign", 10),
            1: ("unknown", 50),
            2: ("malicious", 90),
            3: ("unknown", 50),
        }

        verdict, confidence = verdict_map[bucket]
        result = EnrichmentResult(
            vendor=self.vendor,
            ioc=ioc,
            verdict=verdict,
            confidence=confidence,
            details={"sha256_prefix": digest[:8]},
        )

        self.cache.set(cache_key, result.model_dump())
        return result
    
    def enrich_many(self, iocs: List[IOC]) -> List[EnrichmentResult]:
        return [self.enrich_ioc(ioc) for ioc in iocs]   