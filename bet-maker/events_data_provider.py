from typing import List
from models import EventDB
import aiohttp
import time


class EventsDataProvider:
    events: List[EventDB]
    _last_time: int = 0
    _cache_max_time = 10
    _line_provider_host: str | None = None

    def __init__(self, line_provider_host: str):
        self._line_provider_host = line_provider_host

    async def get_events(self) -> List[EventDB]:
        now = int(time.time())
        if now - self._last_time > self._cache_max_time:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://{self._line_provider_host}/events') as resp:
                    self._last_time = now
                    self.events = [EventDB(**e) for e in await resp.json()]
                    return self.events
        else:
            return self.events

