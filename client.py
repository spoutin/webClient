import random
import asyncio
from aiohttp import ClientSession

async def fetch(url, session):
    async with session.get(url) as response:
        date = response.headers.get("DATE")
        #print("{}:{} content {}".format(date, response.url, response.text()))
        return await response.read()

async def parse(url, session):
    response = await fetch(url, session)
    print(response)
    return response


async def bound_fetch(sem, url, session):
    # Getter function with semaphore.
    async with sem:
        await parse(url, session)


async def run(loop,  r):
    url = "http://localhost:8080/{}"
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(1000)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession(headers={}) as session:
        for i in range(r):
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, url.format(i), session))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses

number = 10000
loop = asyncio.get_event_loop()

future = asyncio.ensure_future(run(loop, number))
loop.run_until_complete(future)