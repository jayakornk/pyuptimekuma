"""Uptime Kuma exceptions."""


class UptimeKumaException(Exception):
    """Base Uptime Kuma exception."""


class UptimeKumaConnectionException(UptimeKumaException):
    """Uptime Kuma connection exception."""


class UptimeKumaAuthenticationException(UptimeKumaException):
    """Uptime Kuma authentication exception."""
