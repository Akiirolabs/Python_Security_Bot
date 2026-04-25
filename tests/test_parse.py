from pathlib import Path

from socbot.parse import load_alerts


def test_load_alerts_csv(tmp_path: Path):
    csv_file = tmp_path / "alerts.csv"
    csv_file.write_text(
        "alert_id,timestamp,source,message\n"
        "A1,2026-04-08T00:00:00Z,EDR,connect to https://evil.com/path\n",
        encoding="utf-8",
    )

    alerts = load_alerts(str(csv_file))
    assert len(alerts) == 1
    assert alerts[0].alert_id == "A1"
    assert len(alerts[0].iocs) >= 1
