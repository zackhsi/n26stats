# Trusty is Travis CI's latest LTS.
FROM ubuntu:trusty

ENV \
    DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    TERM=xterm-color

RUN : \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
        build-essential \
        curl \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes \
    && apt-get update \
    && apt-get install -y python3.6-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && :

RUN : \
    && curl https://bootstrap.pypa.io/get-pip.py | sudo python3.6 \
    && pip install pipenv --upgrade \
    && :

WORKDIR /code/n26stats

COPY Pipfile Pipfile.lock /code/n26stats/
RUN pipenv install --dev --ignore-pipfile

COPY . /code/n26stats/

EXPOSE 8000
CMD pipenv run gunicorn app:n26stats --bind 0.0.0.0:8000 --worker-class aiohttp.worker.GunicornWebWorker

