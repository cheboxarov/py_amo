import asyncio


async def repository_safe_request(request, semaphore, index, *args, **kwargs):
    async with semaphore:
        if index > 0 and index % 5 == 0:
            await asyncio.sleep(1)
        return await request(*args, **kwargs)