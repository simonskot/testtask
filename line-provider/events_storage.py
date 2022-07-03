import time

from models import EventDB, Event, EventStatus
from typing import Iterable, Dict


class EventsStorage:
    _storage: Dict[int, EventDB] = {
        1: EventDB(id=1, win_koef=1.42, bet_deadline=int(time.time()) + 60, status=EventStatus.NOT_HAPPENED_YET),
        2: EventDB(id=2, win_koef=1.14, bet_deadline=int(time.time()) - 60, status=EventStatus.TEAM_ONE_WIN),
        3: EventDB(id=3, win_koef=1.54, bet_deadline=int(time.time()) + 600, status=EventStatus.TEAM_ONE_WIN),
        4: EventDB(id=4, win_koef=1.7, bet_deadline=int(time.time()) + 200, status=EventStatus.NOT_HAPPENED_YET),
    }
    _last_id: int = 4

    def get_new_id(self):
        id = self._last_id + 1
        self._last_id = id
        return id

    async def save_event(self, event: Event) -> EventDB:
        new_id = self.get_new_id()
        db_event = EventDB(id=new_id, **event.dict())
        self._storage[new_id] = db_event
        return db_event

    async def get_event(self, id: int) -> EventDB:
        return self._storage.get(id)

    async def get_events(self) -> Iterable[EventDB]:
        return self._storage.values()
