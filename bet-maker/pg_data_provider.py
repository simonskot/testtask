from models import Bet, BetDB
import asyncpg
from asyncpg.pool import Pool


import logging
logger = logging.getLogger(__name__)


class PGDataProvider:
    _pool: Pool
    _dbname: str = 'test'
    _bet_table_name: str = 'bet'
    host: str
    port: int
    user: str
    password: str

    def __init__(self, host: str, port: int, user: str, password: str):
        self.host = host
        self.user = user
        self.port = port
        self.password = password

    async def start(self):
        self._pool = await asyncpg.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self._dbname,
        )

    async def get_bet(self, id: int) -> BetDB:
        try:
            async with self._pool.acquire() as c:
                r = await c.fetchrow(f"SELECT * FROM {self._bet_table_name} where id=$1", id)
        except asyncpg.PostgresError as e:
            # Some logging here
            raise

        if not r:
            return r

        return BetDB(**{k: v for k, v in r.items()})

    async def save_bet(self, bet: Bet) -> BetDB:
        try:
            async with self._pool.acquire() as c:
                r = await c.fetchrow(
                    f"INSERT INTO {self._bet_table_name} (event_id, amount) VALUES ($1, $2) RETURNING *;",
                    bet.event_id, bet.amount)
        except asyncpg.PostgresError as e:
            # Some logging here
            raise

        return BetDB(**{k: v for k, v in r.items()})
