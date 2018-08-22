[![Build Status](https://travis-ci.org/zackhsi/n26stats.svg?branch=master)](https://travis-ci.org/zackhsi/n26stats)
![Docker Pulls](https://img.shields.io/docker/pulls/zackhsi/n26stats.svg)

n26stats
========

`n26stats` computes realtime statistics for the last 60 seconds of
"transactions".

Usage:

```sh
$ docker run zackhsi/n26stats
```

Running this command will start a web server listening on port 8000.

API
---

`POST /transactions` – Create a new transaction.

`GET /statistics` – Return statistics based on the transactions that happened
in the last 60 seconds.

`DELETE /transactions` – Delete all existing transactions.

Architecture
------------

Under the hood, there is a web tier leveraging
[aiohttp](https://github.com/aio-libs/aiohttp) as the HTTP framework.

The core logic of updating and expiring stats lives in
[stats.py](https://github.com/zackhsi/n26stats/blob/master/n26stats/stats.py).
In order to get statistics in O(1) time, we precompute the statistics upon
ingest and expiry.

Min and max are maintained with a heap. POST will immediately add to both the
min and max heaps. POST will then schedule a
[Future](https://docs.python.org/3/library/asyncio-task.html#future) to sweep /
expire stale values one minute in the future.

Money is represented using the built in
[Decimal](https://docs.python.org/3/library/decimal.html) library. When
presenting statistics via the GET API, we round towards 0 with two decimal
places. However, intermediary calculations such as sum are performed with much
higher precision.

There are extensive test cases in the
[/tests](https://github.com/zackhsi/n26stats/tree/master/tests)
directory.
