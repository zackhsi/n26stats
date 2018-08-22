class N26StatsError(Exception):
    pass


class StatTooOld(N26StatsError):
    """A stat older than one minute is not allowed."""


class StatInTheFuture(N26StatsError):
    """A stat in the future is not allowed."""
