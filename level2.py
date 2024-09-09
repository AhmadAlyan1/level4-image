import aiohttp
import asyncio

async def fetch_batch(session, base_url, start, end):
    async with session.get(f"{base_url}?start={start}&end={end}") as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Error fetching batch {start}-{end}. Status code: {response.status}")
            return []


async def fetch_until_flag(base_url, batch_size=1000):
    start = 0
    found_flag = None
    async with aiohttp.ClientSession() as session:
        while not found_flag:
            end = start + batch_size
            print(f"Fetching data from {start} to {end}...")

            data = await fetch_batch(session, base_url, start, end)

            if not data:
                print("No more data available, flag not found.")
                break

            for entry in data:
                if "flag" in entry:
                    print(f"Flag found: {entry}")
                    found_flag = entry
                    break

            if not found_flag:
                start = end + 1

    return found_flag


# Example usage
base_url = "http://34.69.146.51:5000/level2/"
flag = asyncio.run(fetch_until_flag(base_url))
if flag:
    print(f"Flag: {flag}")
else:
    print("Flag not found.")
