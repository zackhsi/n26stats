from datetime import datetime, timedelta
from decimal import Decimal

import pytest
from pytest_mock import MockFixture

from n26stats import stats
from n26stats.exceptions import StatTooOld


@pytest.fixture(autouse=True)
def reset_stats_container(mocker: MockFixture) -> None:
    mocker.patch.object(
        stats,
        'stats_container',
        return_value=stats.StatsContainer()
    )


def test_empty() -> None:
    expected_stats = {
        'avg': Decimal(0),
        'count': Decimal(0),
        'max': Decimal(0),
        'min': Decimal(0),
        'sum': Decimal(0),
    }
    assert stats.get() == expected_stats


def test_add() -> None:
    now = datetime.now()
    stats.add(
        amount=Decimal(10),
        ts=now,
    )
    expected_stats = {
        'avg': Decimal(10),
        'count': Decimal(1),
        'max': Decimal(10),
        'min': Decimal(10),
        'sum': Decimal(10),
    }
    assert stats.get() == expected_stats

    stats.add(
        amount=Decimal(-5),
        ts=now,
    )
    expected_stats = {
        'avg': Decimal(2.5),
        'count': Decimal(2),
        'max': Decimal(10),
        'min': Decimal(-5),
        'sum': Decimal(5),
    }
    assert stats.get() == expected_stats


def test_stat_too_old() -> None:
    stats.add(
        amount=Decimal(10),
        ts=datetime.now() - timedelta(seconds=59)
    )
    with pytest.raises(StatTooOld):
        stats.add(
            amount=Decimal(10),
            ts=datetime.now() - timedelta(seconds=60)
        )


def test_remove() -> None:
    now = datetime.now()
    stats.add(
        amount=Decimal(10),
        ts=now,
    )
