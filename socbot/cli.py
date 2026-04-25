from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from .cache import DiskTTLCache
from .enrichers import MockEnricher
from .logging_setup import setup_logging
from .models import Case, IOC
from .parse import load_alerts
from .report import write_case_json, write_report_md
from .scoring import compute_score, recommendation_from_severity

def run_pipeline(input_path: str, out_dir: str, enrichment_mode: str = "mock") -> None:
    cofig_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(config_path)

    with open(config_file, "r") as f:
        config = yaml.safe_load(handle) or {}
        
    logger = setup_logging(out_dir)
    logger.info("Starting pipeline")
    logger.info("Input=%s" Out=%s Config=%s, input_path, out_dir, config_path)

    alerts = load_alerts(input_path)
    logger.info("Loaded %d alerts from %s", len(alerts), input_path)

    deduped_iocs: dict[str, IOC] = {}
    for alert in alerts:
        for ioc in alert.iocs:
            deduped_iocs[f"{ioc.type}:{ioc.normalized}"] = ioc
            