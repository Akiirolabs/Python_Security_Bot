from __future__ import annotations

import logging
from pathlib import Path


def setup_logging(out_dir: str) -> logging.Logger:
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    log_path = Path(out_dir) / "run.log"

    logger = logging.getLogger("socbot")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger




