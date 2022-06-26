# pyuptimekuma
Simple Python wrapper for Uptime Kuma

## Installation

```shell
python3 -m pip install pyuptimekuma
```

## Example

```python
import asyncio

import aiohttp

from pyuptimekuma import UptimeKuma

URL = ""
USERNAME = ""
PASSWORD = ""
VERIFY_SSL = True


async def main():

    async with aiohttp.ClientSession() as session:
        uptime_robot_api = UptimeKuma(session, URL, USERNAME, PASSWORD, VERIFY_SSL)
        response = await uptime_robot_api.async_get_monitors()
        print(response.data)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

```

## Credit

I would like to give a special thanks to these repositories since a lot of code has been inspired by them.

- [ludeeus/pyuptimerobot](https://github.com/ludeeus/pyuptimerobot)
- [meichthys/utptime_kuma_monitor](https://github.com/meichthys/utptime_kuma_monitor)