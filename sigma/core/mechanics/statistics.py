import json

import aiohttp


class ElasticHandler(object):
    def __init__(self, url, index):
        self.url = url
        self.type = index

    async def post(self, data):
        qry = json.dumps(data)
        api_url = f'{self.url}/{self.type}/doc/'
        heads = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            await session.post(api_url, data=qry, headers=heads)
