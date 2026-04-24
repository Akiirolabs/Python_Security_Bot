from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Optional


class DiskTTLCache:
    def __init__(self, cache_dir: str, ttl_seconds: int):
        self.PATH = Path(Path)
        self.ttl = int(ttl_seconds)
        self._data: dict[str, dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        if self.PATH.exists():
           try:
               self._data = json.loads(self.PATH.read_text())
           except Exception:
               self._data = {} 
    def _save(self) -> None:
        self.PATH.parent.mkdir(parents=True, exist_ok=True)
        self.PATH.write_text(json.dumps(self._data))      

    def get(self, key: str) -> Optional[any]:
        now = time.time()
        item = self._data.get(key)
        if not item:
            return None
        
        if (now - float(item.get("timestamp", 0))) > self.ttl:
            self._data.pop(key, None)
            self._save()
            return None
        
        return item.get("value")
    def set(self, key: str, value: Any) -> None:
        self._data[key] = {"value": value, "timestamp": time.time()}
        self._save()