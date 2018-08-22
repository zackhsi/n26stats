"""
Stats contains functions for interacting with the global in-memory stats.

Max and min are stored with heaps.

Getting statistics is O(1) because we precompute them on statistic entry and
statistic expiry.
"""
import logging
from asyncio import ensure_future, sleep
from datetime import datetime, timedelta
from decimal import Decimal
from heapq import heapify, heappush
from typing import Dict, List, Tuple

from n26stats import money
from n26stats.exceptions import StatInTheFuture, StatTooOld

logger = logging.getLogger(__name__)


class StatsContainer:
    def __init__(self) -> None:
        self.sweep_futures: List = []
        self.reset()
        logger.info('Initialized stats container')

    def reset(self) -> None:
        self.count: int = 0
        self.sum: Decimal = Decimal('0')
        self.min_heap: List[Tuple[Decimal, datetime]] = []
        self.max_heap: List[Tuple[Decimal, datetime]] = []
        for sweep_future in self.sweep_futures:
            sweep_future.cancel()
        self.sweep_futures = []
        logger.info('Reset stats container')

    def add(self, amount: Decimal, ts: datetime) -> None:
        now = datetime.now()
        if ts < now - timedelta(minutes=1):
            raise StatTooOld()
        if ts > now:
            raise StatInTheFuture

        self.count = self.count + 1
        self.sum = self.sum + amount

        # `heappush` assumes a min heap. We negate the amount in order to
        # implement a max heap.
        heappush(self.min_heap, (amount, ts))
        heappush(self.max_heap, (-amount, ts))
        logger.info(f'Added {amount} at {ts}')

    @property
    def min(self) -> Decimal:
        if not self.min_heap:
            return Decimal('0')
        return self.min_heap[0][0]

    @property
    def max(self) -> Decimal:
        if not self.max_heap:
            return Decimal('0')
        return self.max_heap[0][0] * -1

    @property
    def avg(self) -> Decimal:
        if self.count:
            return money.quantize(self.sum / self.count)
        else:
            return Decimal('0')

    def sweep(self) -> None:
        for heap_name in ['min_heap', 'max_heap']:
            old_heap = getattr(self, heap_name)
            new_heap = []
            for amount, ts in old_heap:
                if self.is_expired(ts):
                    if heap_name == 'min_heap':
                        # Use the non-negated min_heap amounts to update
                        # statistics.
                        self.count = self.count - 1
                        self.sum = self.sum - amount
                else:
                    new_heap.append((amount, ts))
            heapify(new_heap)
            setattr(self, heap_name, new_heap)
        logger.info('Swept!')

    def is_expired(self, ts: datetime) -> bool:
        now = datetime.now()
        return ts < now - timedelta(minutes=1)

    def statistics(self) -> Dict:
        return {
            'avg': self.avg,
            'count': self.count,
            'max': self.max,
            'min': self.min,
            'sum': self.sum,
        }


_stats_container = StatsContainer()


def stats_container() -> StatsContainer:
    global _stats_container
    return _stats_container


def get() -> Dict:
    return stats_container().statistics()


def add(amount: Decimal, ts: datetime) -> None:
    stats_container().add(
        amount=amount,
        ts=ts,
    )


def sweep() -> None:
    stats_container().sweep()


async def _sweep_at(ts: datetime) -> None:
    now = datetime.now()
    if ts < now:
        raise Exception('Cannot schedule sweep in the past')

    delta_seconds = (ts - now).total_seconds()
    await sleep(delta_seconds)
    sweep()


async def sweep_at(ts: datetime) -> None:
    sweep_future = ensure_future(_sweep_at(ts))
    stats_container().sweep_futures.append(sweep_future)


def reset() -> None:
    stats_container().reset()
