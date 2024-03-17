import abc
import asyncio
from typing import Optional

import arrow

from sigma.core.mechanics.database import Database

EXPIRATION = 60


class RelayHandler(abc.ABC):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.storage = {}

    async def store(self, token: str, cid: int, uname: str, msg: str):
        now = arrow.utcnow().float_timestamp
        doc = {
            'channel_id': cid,
            'user_name': uname,
            'message': msg,
            'token': token,
            'timestamp': now,
            'finished': False,
            'response': None
        }
        await self.db.col.AIRelay.insert_one(doc)

    async def clean(self):
        now = arrow.utcnow().float_timestamp
        self.db.col.AIRelay.delete_many({'timestamp': {'$lt': now - EXPIRATION}})

    async def remove(self, token: str):
        await self.db.col.AIRelay.delete_one({'token': token})

    async def wait_for_reply(self, token: str) -> Optional[str]:
        start = arrow.utcnow().float_timestamp
        doc = None
        while doc is None:
            doc = await self.db.col.AIRelay.find_one({'token': token, 'finished': True})
            if not doc:
                now = arrow.utcnow().float_timestamp
                if now > (start + EXPIRATION):
                    break
                else:
                    await asyncio.sleep(1)
        msg = None
        if doc:
            msg = doc.get('response')
        return msg
