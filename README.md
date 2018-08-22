[![Build Status](https://travis-ci.org/zackhsi/n26stats.svg?branch=master)](https://travis-ci.org/zackhsi/n26stats)
![Docker Pulls](https://img.shields.io/docker/pulls/zackhsi/n26stats.svg)

n26stats
========

`n26stats` computes realtime statistics for the last 60 seconds of
"transactions".

API
---

`POST /transactions` – Create a new transaction.

`GET /statistics` – Return statistics based on the transactions that happened
in the last 60 seconds.

`DELETE /transactions` – Delete all existing transactions.
