"""Шаг 4: сравнение блокировки, потока и процессов.

Запуск из корня проекта:
    .venv/bin/python starter/step4_blocking.py --mode blocking
    .venv/bin/python starter/step4_blocking.py --mode thread
    .venv/bin/python starter/step4_blocking.py --mode process
    .venv/bin/python starter/step4_blocking.py --mode thread --heavy three
    .venv/bin/python starter/step4_blocking.py --mode process --heavy three

По умолчанию тяжёлый только bob. В режиме three тяжёлые bob, dave и eve.
Время вычислений зависит от компьютера и числа доступных процессоров.
"""

import argparse
import asyncio
from concurrent.futures import ProcessPoolExecutor

from timer import log, print_time

CLIENTS = [
    ("alice", 0.5),
    ("bob", 5.0),
    ("carol", 0.5),
    ("dave", 0.5),
    ("eve", 0.5),
]


def heavy_compute() -> int:
    """Синхронные тяжёлые вычисления, 1-3 секунды."""
    h = 0
    for i in range(30_000_000):
        h = (h * 31 + i) & 0xFFFFFFFF
    return h


async def handle_request(
    client: str,
    duration: float,
    heavy_clients: set[str],
    mode: str,
    pool: ProcessPoolExecutor | None,
) -> None:
    log(f"{client}: запрос принят")
    if client not in heavy_clients:
        await asyncio.sleep(duration)
    elif mode == "blocking":
        heavy_compute()
    elif mode == "thread":
        await asyncio.to_thread(heavy_compute)
    else:
        if pool is None:
            raise RuntimeError("Для режима process нужен пул процессов")
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(pool, heavy_compute)
    log(f"{client}: ответ отправлен")


async def run_requests(
    mode: str, heavy_clients: set[str], pool: ProcessPoolExecutor | None
) -> None:
    coroutines = [
        handle_request(client, duration, heavy_clients, mode, pool)
        for client, duration in CLIENTS
    ]
    await asyncio.gather(*coroutines)


async def main(mode: str, heavy: str) -> None:
    heavy_clients = {"bob"} if heavy == "bob" else {"bob", "dave", "eve"}
    if mode == "process":
        with ProcessPoolExecutor(max_workers=len(heavy_clients)) as pool:
            await run_requests(mode, heavy_clients, pool)
    else:
        await run_requests(mode, heavy_clients, None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("blocking", "thread", "process"), default="blocking")
    parser.add_argument("--heavy", choices=("bob", "three"), default="bob")
    args = parser.parse_args()
    print(f"Режим: {args.mode}; тяжёлые клиенты: {args.heavy}")
    with print_time():
        asyncio.run(main(args.mode, args.heavy))
