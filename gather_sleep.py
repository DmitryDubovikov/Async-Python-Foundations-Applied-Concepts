
import asyncio
from datetime import datetime


async def sleep_five():
    print("start sleep 5")
    await asyncio.sleep(5)
    print("end sleep 5")


async def sleep_three_then_five():
    print("start sleep 3 then 5")
    await asyncio.sleep(3)
    await sleep_five()
    print("end sleep 3 then 5")


async def main():
    await asyncio.gather(sleep_five(), sleep_three_then_five())
    


start = datetime.now()
asyncio.run(main())
print(f"time: {datetime.now()-start}")