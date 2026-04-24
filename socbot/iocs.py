from __future__ import annotations

import ipaddress
import re
from urllib.parse import urlparse

from .models import IOC

HASH_RE = re.compile(r"\b([A-Fa-f0-9]{32}|[A-Fa-f0-9]{64})\b")
DOMAIN_RE = re.compile(r"\b((?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})\b")
IP_RE = re.compile(r"\b(\d{1,3}(?:\.\d{1,3}){3})\b")
URL_RE = re.compile(r"\bhttps?://[^\s/$.?#][^\s]*\b", re.IGNORECASE)


def _is_valid_ip(s: str) -> bool:
    try:
        ipaddress.ip_address(s)
        return True
    except ValueError:
        return False


def normalize_ioc(ioc_type: str, raw: str) -> str:
    raw = raw.strip()
    if ioc_type == "domain":
        return raw.lower().rstrip(".")
    if ioc_type == "url":
        p = urlparse(raw)
        scheme = (p.scheme or "http").lower()
        host = (p.hostname or "").lower()
        path = p.path or ""
        return f"{scheme}://{host}{path}"
    if ioc_type == "hash":
        return raw.lower()
    if ioc_type == "ip":
        return raw
    return raw


def classify_and_build(raw: str) -> IOC | None:
    raw = raw.strip()
    if not raw:
        return None

    if raw.lower().startswith(("http://", "https://")):
        return IOC(type="url", value=raw, normalized=normalize_ioc("url", raw))

    if _is_valid_ip(raw):
        return IOC(type="ip", value=raw, normalized=normalize_ioc("ip", raw))

    if HASH_RE.fullmatch(raw):
        return IOC(type="hash", value=raw, normalized=normalize_ioc("hash", raw))

    domain_candidate = raw.rstrip(".")
    if DOMAIN_RE.fullmatch(domain_candidate):
        return IOC(type="domain", value=raw, normalized=normalize_ioc("domain", domain_candidate))

    return None


def extract_iocs_from_text(text: str) -> list[str]:
    found: set[str] = set()
    found.update(URL_RE.findall(text))
    found.update(IP_RE.findall(text))
    found.update(DOMAIN_RE.findall(text))
    found.update(HASH_RE.findall(text))
    return sorted(found)