from datetime import datetime, timedelta

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
        'avg': 0,
        'count': 0,
        'max': 0,
        'min': 0,
        'sum': 0,
    }
    assert stats.get() == expected_stats


def test_add() -> None:
    now = datetime.now()
    stats.add(
        amount=10,
        ts=now,
    )
    expected_stats = {
        'avg': 10.0,
        'count': 1,
        'max': 10,
        'min': 10,
        'sum': 10,
    }
    assert stats.get() == expected_stats

    stats.add(
        amount=-5,
        ts=now,
    )
    expected_stats = {
        'avg': 2.5,
        'count': 2,
        'max': 10,
        'min': -5,
        'sum': 5,
    }
    assert stats.get() == expected_stats


def test_stat_too_old() -> None:
    stats.add(
        amount=10,
        ts=datetime.now() - timedelta(seconds=59)
    )
    with pytest.raises(StatTooOld):
        stats.add(
            amount=10,
            ts=datetime.now() - timedelta(seconds=60)
        )
