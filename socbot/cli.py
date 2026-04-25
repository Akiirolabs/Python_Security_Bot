from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Optional

import yaml

from .cache import DiskTTLCache
from .enrichers import MockEnricher
from .logging_setup import setup_logging
from .models import Case, IOC
from .parse import load_alerts
from .report import write_case_json, write_report_md
from .scoring import compute_score, recommendation_from_severity, severity_from_score


def run_pipeline(
    input_path: str,
    out_dir: str,
    config_path: str = "config.yaml",
    enrichment_mode: str = "mock",
) -> Case:
    config = _load_config(config_path)
    logger = setup_logging(out_dir)
    logger.info("Starting pipeline")
    logger.info("Input=%s Out=%s Config=%s", input_path, out_dir, config_path)

    alerts = load_alerts(input_path)
    logger.info("Loaded %d alerts from %s", len(alerts), input_path)

    deduped_iocs: dict[str, IOC] = {}
    for alert in alerts:
        for ioc in alert.iocs:
            deduped_iocs[f"{ioc.type}:{ioc.normalized}"] = ioc

    iocs = list(deduped_iocs.values())
    logger.info("Extracted %d unique IOCs", len(iocs))

    if enrichment_mode != "mock":
        raise ValueError(f"Unsupported enrichment mode: {enrichment_mode}")

    cache_dir = str(config.get("cache_dir", Path(out_dir) / ".cache"))
    cache_ttl_seconds = int(config.get("cache_ttl_seconds", 3600))
    enricher = MockEnricher(DiskTTLCache(cache_dir, cache_ttl_seconds))
    enrichments = enricher.enrich_many(iocs)

    score = compute_score(enrichments, config.get("risk_weights"))
    severity = severity_from_score(score)
    case = Case(
        alerts=alerts,
        iocs=iocs,
        enrichments=enrichments,
        score=score,
        severity=severity,
        recommendations=recommendation_from_severity(severity),
    )

    case_path = write_case_json(case, out_dir)
    report_path = write_report_md(case, out_dir)
    logger.info("Wrote %s and %s", case_path, report_path)
    return case


def validate_input(input_path: str) -> int:
    alerts = load_alerts(input_path)
    ioc_count = sum(len(alert.iocs) for alert in alerts)
    print(f"OK: loaded {len(alerts)} alerts and extracted {ioc_count} IOCs")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="socbot")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate an alert input file")
    validate.add_argument("--input", required=True, dest="input_path")

    run = subparsers.add_parser("run", help="Run the SOC automation pipeline")
    run.add_argument("--input", required=True, dest="input_path")
    run.add_argument("--output", required=True, dest="out_dir")
    run.add_argument("--config", default="config.yaml", dest="config_path")
    run.add_argument("--enrichment-mode", default="mock", choices=["mock"])

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate":
        return validate_input(args.input_path)
    if args.command == "run":
        run_pipeline(args.input_path, args.out_dir, args.config_path, args.enrichment_mode)
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


def _load_config(config_path: str) -> dict[str, Any]:
    path = Path(config_path)
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


if __name__ == "__main__":
    raise SystemExit(main())
