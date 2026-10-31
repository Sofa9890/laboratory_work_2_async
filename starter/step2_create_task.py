"""Дополнение к шагу 2б: те же десять ожиданий через create_task."""

import asyncio

from timer import print_time


async def work(n: int) -> None:
    print(f"start {n}")
    await asyncio.sleep(1)
    print(f"done {n}")


async def main() -> None:
    tasks = [asyncio.create_task(work(n)) for n in range(1, 11)]
    for task in tasks:
        await task


if __name__ == "__main__":
    with print_time():
        asyncio.run(main())
