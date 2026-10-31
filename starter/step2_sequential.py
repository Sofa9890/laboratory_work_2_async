"""Шаг 2а: корутины запускаются последовательно из-за await в цикле."""

import asyncio

from timer import print_time


async def work(n: int) -> None:
    print(f"start {n}")
    await asyncio.sleep(1)
    print(f"done {n}")


async def main() -> None:
    for n in range(1, 11):
        await work(n)


if __name__ == "__main__":
    with print_time():
        asyncio.run(main())
