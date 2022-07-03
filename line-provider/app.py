import time

from fastapi import FastAPI, HTTPException
from models import Event
from events_storage import EventsStorage

app = FastAPI()
events_storage = EventsStorage()


@app.post('/event')
async def create_event(event: Event):
    r = await events_storage.save_event(event)
    return r


@app.get('/event/{event_id}')
async def get_event(event_id: int):
    r = events_storage.get_event(event_id)
    if not r:
        raise HTTPException(status_code=404, detail="Event not found")

    return r


@app.get('/events')
async def get_events():
    t = time.time()
    raw_events = await events_storage.get_events()
    events = tuple(filter(lambda x: t < int(x.bet_deadline), raw_events))
    return events
