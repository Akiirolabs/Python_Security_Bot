from __future__ import annotations
import json
from pathlib import Path

import pandas as pd

from .iocs import classify_and_build, extract_iocs_from_text
from .models import Alert

def load_alerts(input_path: str) -> list[Alert]:
    p = Path(input_path)
    if not p.exists():
      raise FileNotFoundError("Input_path")

    suffix = p.suffix.lower()
    if suffix == ".csv":
     df = pd.read_csv(p)
    return _alerts_from_dataframe(df)

    raise ValueError(f"Unsupported Input type (use .csv or .json)")

def _alerts_from_dataframe(df: pd.DataFrame) -> list[Alert]:
    required = {"alert_id", "timestamp", "source", "message"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing required columns: {sorted(missing)}")

    alerts: list[Alert] = []
    for _, row in df.iterrows():
        alert = Alert(
            alert_id = str(row["alert_id"]),
            timestamp = str(row["timestamp"]),
            source = str(row["source"]),
            message = str(row["message"]),
        iocs=[],
    )
    ioc_strings = extract_iocs_from_text(alert.message)
    raw_iocs = extract_iocs_from_text(alert.message)
    for raw in raw_iocs:
        ioc = classify_and_build(raw)
        if ioc:
            alert.iocs.append(ioc)

        alerts.append(alert)

    return alerts

