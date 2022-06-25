"""Uptime Kuma constants."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

API_METRICS_URL = "/metrics"
API_HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}

ATTR_URL = "url"