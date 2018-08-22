"""
Stats contains functions for interacting with the global in-memory stats.

Max and min are stored with heaps.

Getting statistics is O(1) because we precompute them on statistic entry and
statistic expiry.
"""
from datetime import datetime, timedelta
from decimal import Decimal
from heapq import heappush
from typing import Dict, List, Tuple

from n26stats.exceptions import StatTooOld


class StatsContainer:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.avg: Decimal = Decimal(0)
        self.count: Decimal = Decimal(0)
        self.sum: Decimal = Decimal(0)
        self.min_heap: List[Tuple[Decimal, datetime]] = []
        self.max_heap: List[Tuple[Decimal, datetime]] = []

    def add(self, amount: Decimal, ts: datetime) -> None:
        now = datetime.now()
        if ts < now - timedelta(minutes=1):
            raise StatTooOld()

        self.count = self.count + 1
        self.sum = self.sum + amount

        # Average depends on sum and count.
        self.avg = self.sum / self.count

        # `heappush` assumes a min heap. We negate the amount in order to
        # implement a max heap.
        heappush(self.min_heap, (amount, ts))
        heappush(self.max_heap, (-amount, ts))

    @property
    def min(self) -> Decimal:
        if not self.min_heap:
            return Decimal(0)
        return self.min_heap[0][0]

    @property
    def max(self) -> Decimal:
        if not self.max_heap:
            return Decimal(0)
        return self.max_heap[0][0] * -1

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
                        # Average depends on sum and count.
                        if self.count:
                            self.avg = self.sum / self.count
                        else:
                            self.avg = Decimal(0)
                else:
                    new_heap.append((amount, ts))
            setattr(self, heap_name, new_heap)

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
