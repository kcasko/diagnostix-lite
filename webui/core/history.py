"""
History tracking for system snapshots.
"""
import os
import platform
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

import psutil

from core.db import db_instance


class HistoryTracker:
    """Track system metrics over time for trending."""

    @staticmethod
    def _default_disk_path() -> str:
        system = platform.system()
        if system == "Windows":
            return f"{os.environ.get('SystemDrive', 'C:')}\\"
        return "/"

    @staticmethod
    def collect_snapshot() -> Dict[str, Any]:
        cpu_usage = psutil.cpu_percent(interval=0.1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage(HistoryTracker._default_disk_path()).percent
        return {
            "timestamp": datetime.now().isoformat(),
            "hostname": platform.node(),
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "disk_usage": disk_usage,
        }

    @staticmethod
    def record_snapshot(metrics: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if metrics is None:
            metrics = HistoryTracker.collect_snapshot()
        if db_instance.conn is None:
            try:
                db_instance.connect()
            except Exception:
                return metrics
        db_instance.log_snapshot(
            hostname=metrics.get("hostname", platform.node()),
            cpu_usage=metrics.get("cpu_usage"),
            memory_usage=metrics.get("memory_usage"),
            disk_usage=metrics.get("disk_usage"),
        )
        return metrics

    @staticmethod
    def get_trend(metric: str, days: int = 7) -> List[Dict[str, Any]]:
        return db_instance.get_trend(metric, days)
