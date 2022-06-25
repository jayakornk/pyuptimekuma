"""Decorator for Uptime Kuma"""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import aiohttp

from pyuptimekuma import exceptions

from .const import LOGGER
from .models import UptimeKumaApiResponse

if TYPE_CHECKING:
    from .uptimekuma import UptimeKuma


def api_request(api_path: str, method: str = "GET"):
    """Decorator for Uptime Kuma API request"""

    def decorator(func):
        """Decorator"""

        async def wrapper(*args, **kwargs):
            """Wrapper"""
            client: UptimeKuma = args[0]
            url = f"{client._base_url}{api_path}"
            LOGGER.debug("Requesting %s", url)
            try:
                request = await client._session.request(
                    method=method,
                    url=url,
                    timeout=aiohttp.ClientTimeout(total=10),
                    auth=aiohttp.BasicAuth(client._username, client._password),
                    verify_ssl=client._verify_ssl,
                )

                if request.status != 200:
                    raise exceptions.UptimeKumaConnectionException(
                        f"Request for '{url}' failed with status code '{request.status}'"
                    )

                result = await request.text()
            except aiohttp.ClientError as exception:
                raise exceptions.UptimeKumaConnectionException(
                    f"Request exception for '{url}' with - {exception}"
                ) from exception

            except asyncio.TimeoutError:
                raise exceptions.UptimeKumaConnectionException(
                    f"Request timeout for '{url}'"
                ) from None

            except exceptions.UptimeKumaConnectionException as exception:
                raise exceptions.UptimeKumaConnectionException(exception) from exception

            except exceptions.UptimeKumaException as exception:
                raise exceptions.UptimeKumaException(exception) from exception

            except (Exception, BaseException) as exception:
                raise exceptions.UptimeKumaException(
                    f"Unexpected exception for '{url}' with - {exception}"
                ) from exception

            LOGGER.debug("Requesting %s returned %s", url, result)

            # print(result)
            response = UptimeKumaApiResponse.from_prometheus(
                {"monitors": result, "_api_path": api_path, "_method": method}
            )

            return response

        return wrapper

    return decorator
