from __future__ import annotations
from typing import Any, Dict, List, Optional, Literal
from pydantic import BaseModel, Field

IOCType = Literal["ip", "domain", "url", "hash"]
Verdict = Literal["malicious", "benign", "unknown"]
Severity = Literal["low", "medium", "high", "critical"]

class IOC(BaseModel):
    type: IOCType
    value: str
    normalized: str

class Alert(BaseModel):
    alert_id: str
    timestamp: str
    source: str
    message: str
    iocs: List[IOC] = Field(default_factory=list)

class EnrichmentResult(BaseModel):
    ioc: IOC
    verdict: Verdict
    severity: Severity
    details: Optional[Dict[str, Any]] = None

class Case(BaseModel):
    alerts: List[Alert] 
    iocs: List[IOC] 
    enrichment_results: List[EnrichmentResult] 
    score: int= Field  (ge=0, le=100)
    Severity: Severity
    recommendation: List[str] = Field(default_factory=list) 