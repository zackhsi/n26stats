"""
Stats contains functions for interacting with the global in-memory stats.
"""
from datetime import datetime, timedelta
from typing import Dict

from n26stats.exceptions import StatTooOld


class StatsContainer:
    def __init__(self) -> None:
        self.reset_stats()

    def reset_stats(self) -> None:
        self.avg = 0.0
        self.count = 0
        self.max = 0
        self.min = 0
        self.sum = 0

    def add(self, amount: int, ts: datetime) -> None:
        now = datetime.now()
        if ts < now - timedelta(minutes=1):
            raise StatTooOld()

        if self.count == 0:
            self.max = amount
            self.min = amount
        else:
            self.max = max(self.max, amount)
            self.min = min(self.min, amount)

        self.count = self.count + 1
        self.sum = self.sum + amount

        # Average depends on sum and count.
        self.avg = self.sum / self.count

    def remove(self, value: int) -> None:
        pass

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


def add(amount: int, ts: datetime) -> None:
    stats_container().add(
        amount=amount,
        ts=ts,
    )
