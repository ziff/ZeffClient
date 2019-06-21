FROM python:3

MAINTAINER "Lance Finn Helsten" <lanhel@flyingtitans.com>

WORKDIR /usr/src/zeffclient

COPY . /usr/src/zeffclient

RUN pip install --upgrade pip && \
    pip install -e ".[dev]"

CMD [ "python", "setup.py", "build" ]

