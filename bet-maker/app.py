import time
from fastapi import FastAPI, HTTPException
from fastapi.openapi.models import Response

from models import Bet, EventDB, BetDB
from config import APP_VERSION, DEBUG, POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_PORT, \
    LINE_PROVIDER_HOST
from typing import List
from pg_data_provider import PGDataProvider
from events_data_provider import EventsDataProvider


fast_api_config = {
    "version": APP_VERSION,
    "debug": DEBUG,
    "title": "Bet maker",
    "description": """
    Service for making bets on some events
    """
}

app = FastAPI(**fast_api_config)
pg_data_provider = PGDataProvider(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
)
events_provider = EventsDataProvider(LINE_PROVIDER_HOST)
app.add_event_handler("startup", pg_data_provider.start)


@app.get("/events", response_model=List[EventDB])
async def events():
    return await events_provider.get_events()


@app.post("/bet", response_model=BetDB)
async def post_bet(bet: Bet):
    all_events = await events_provider.get_events()
    all_events = {e.id: e for e in all_events}
    event = all_events.get(bet.event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.bet_deadline < int(time.time()):
        raise HTTPException(status_code=404, detail="Cannot make bet: event unavailable for bet")

    # we can also check event status here

    saved_bet = await pg_data_provider.save_bet(bet)
    return saved_bet


@app.get("/bet/{bet_id}", response_model=BetDB)
async def get_bet(bet_id: int):
    bet = await pg_data_provider.get_bet(bet_id)

    if not bet:
        raise HTTPException(status_code=404, detail="Bet not found")

    return bet
