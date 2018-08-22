from datetime import datetime, timedelta
from decimal import Decimal

import pytest
from freezegun import freeze_time
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


def test_sweep() -> None:
    initial_datetime = datetime(
        year=2018,
        month=10,
        day=17,
        hour=0,
        minute=0,
        second=0,
    )
    with freeze_time(initial_datetime) as frozen_datetime:
        # [
        #     (10, t0),
        # ]
        stats.add(
            amount=Decimal(10),
            ts=datetime.now(),
        )
        expected_stats = {
            'avg': Decimal(10),
            'count': Decimal(1),
            'max': Decimal(10),
            'min': Decimal(10),
            'sum': Decimal(10),
        }
        assert stats.get() == expected_stats

        # [
        #     (10, t0),
        #     (5, t0 + 21),
        # ]
        frozen_datetime.tick(delta=timedelta(seconds=21))
        stats.sweep()
        stats.add(
            amount=Decimal(5),
            ts=datetime.now(),
        )
        expected_stats = {
            'avg': Decimal(7.5),
            'count': Decimal(2),
            'max': Decimal(10),
            'min': Decimal(5),
            'sum': Decimal(15),
        }
        assert stats.get() == expected_stats

        # [
        #     (10, t0),
        #     (5, t0 + 21),
        #     (-3, t0 + 42),
        # ]
        frozen_datetime.tick(delta=timedelta(seconds=21))
        stats.sweep()
        stats.add(
            amount=Decimal(-3),
            ts=datetime.now(),
        )
        expected_stats = {
            'avg': Decimal(4),
            'count': Decimal(3),
            'max': Decimal(10),
            'min': Decimal(-3),
            'sum': Decimal(12),
        }
        assert stats.get() == expected_stats

        # [
        #     (10, t0),  expired
        #     (5, t0 + 21)
        #     (-3, t0 + 42)
        #     (1, t0 + 63)
        # ]
        frozen_datetime.tick(delta=timedelta(seconds=21))
        stats.sweep()
        stats.add(
            amount=Decimal(1),
            ts=datetime.now(),
        )
        expected_stats = {
            'avg': Decimal(1),
            'count': Decimal(3),
            'max': Decimal(5),
            'min': Decimal(-3),
            'sum': Decimal(3),
        }
        assert stats.get() == expected_stats
