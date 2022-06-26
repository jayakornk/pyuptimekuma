"""Uptime Kuma models"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from prometheus_client.parser import text_string_to_metric_families as parser


class MonitorType(str, Enum):
    """Monitors type."""

    HTTP = "http"
    PORT = "port"
    PING = "ping"
    KEYWORD = "keyword"
    DNS = "dns"
    PUSH = "push"
    STEAM = "steam"
    MQTT = "mqtt"
    SQL = "sqlserver"


class UptimeKumaBaseModel:
    """UptimeKumaBaseModel."""


@dataclass
class UptimeKumaMonitor(UptimeKumaBaseModel):
    """Monitor model for Uptime Kuma."""

    monitor_cert_days_remaining: float = 0
    monitor_cert_is_valid: float = 0
    monitor_hostname: str = ""
    monitor_name: str = ""
    monitor_port: str = ""
    monitor_response_time: float = 0
    monitor_status: float = 0
    monitor_type: MonitorType = MonitorType.HTTP
    monitor_url: str = ""

    @staticmethod
    def from_dict(data: dict[str, Any]) -> UptimeKumaMonitor:
        """Generate object from json."""
        obj: dict[str, Any] = {}
        for key, value in data.items():
            if hasattr(UptimeKumaMonitor, key):
                obj[key] = value

        if obj.get("type"):
            obj["type"] = MonitorType(obj["type"])

        return UptimeKumaMonitor(**obj)


@dataclass
class UptimeKumaApiResponse(UptimeKumaBaseModel):
    """API response model for Uptime Kuma."""

    _method: str | None = None
    _api_path: str | None = None
    data: list[UptimeKumaMonitor] | None = None

    @staticmethod
    def from_prometheus(data: dict[str, Any]) -> UptimeKumaApiResponse:
        """Generate object from json."""
        obj: dict[str, Any] = {}
        monitors = []

        for key, value in data.items():
            if hasattr(UptimeKumaApiResponse, key):
                obj[key] = value

        parsed = parser(data["monitors"])
        for family in parsed:
            for sample in family.samples:
                if sample.name.startswith("monitor"):
                    existed = next(
                        (
                            i
                            for i, x in enumerate(monitors)
                            if x["monitor_name"] == sample.labels["monitor_name"]
                        ),
                        None,
                    )
                    if existed is None:
                        temp = {**sample.labels, sample.name: sample.value}
                        monitors.append(temp)
                    else:
                        monitors[existed][sample.name] = sample.value
        obj["data"] = [
            UptimeKumaMonitor.from_dict(monitor) for monitor in monitors
        ]

        return UptimeKumaApiResponse(**obj)
