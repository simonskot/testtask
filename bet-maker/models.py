from enum import IntEnum
from pydantic import BaseModel, Field
from decimal import Decimal


class Bet(BaseModel):
    event_id: int
    amount: Decimal = Field(None, gt=0, decimal_places=2)


class BetDB(Bet):
    id: int


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
