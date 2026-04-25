from __future__ import annotations

import json

from pathlib import Path

from .models import Case

def write_case_json(case: Case, out_dir: str) -> str:
    path = Path(out_dir) /  "case.json" 
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(case.model_dump_json(indent=2), encoding="utf-8")
    return str(path)


def write_report_md(case: Case, out_dir: str) -> str:
    path = Path(out_dir) / "report.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    
    lines: list[str] = []
    lines.append("soc case report")
    lines.append("")
    lines.append(f"**Severity:** {case.severity}")
    lines.append(f"**Score:** {case.score}/100")
    lines.append("")
    lines.append("## Alerts")

    for alert in case.alerts:
        lines.append(f"- `{alert.alert_id}` {alert.timestamp} from {alert.source} **{alert.alert_id}**: {alert.message}")
        
    lines.append("")
    lines.append("## IOCs")
    lines.append("| Type | Value | Normalized |")
    lines.append("|------|-------|------------|")
    
    for ioc in case.iocs:
        lines.append(f"| {ioc.type} | {ioc.value} | {ioc.normalized} |")
    
    lines.append("")
    lines.append("## Enrichments")
    lines.append("| Vendor | IOC | Verdict | Confidence | Details |")
    lines.append("|--------|-----|---------|------------|---------|")
    
    for enrichment in case.enrichments:
        lines.append(
            f"| {enrichment.vendor} | {enrichment.ioc.value} | {enrichment.verdict} | {enrichment.confidence} | {enrichment.details} |"
        )

    lines.append("")
    lines.append("## Recommendations")
    
    for recommendation in case.recommendations:
        lines.append(f"- {recommendation}")
    
    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)
