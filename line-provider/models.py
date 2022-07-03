from pydantic import BaseModel
from enum import IntEnum
from decimal import Decimal


class EventStatus(IntEnum):
    NOT_HAPPENED_YET = 1
    TEAM_ONE_WIN = 2
    TEAM_TWO_WIN = 3


class Event(BaseModel):
    win_koef: Decimal
    bet_deadline: int
    status: EventStatus


class EventDB(Event):
    id: int
