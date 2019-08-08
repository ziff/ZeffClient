FROM python:3

MAINTAINER "Lance Finn Helsten" <lanhel@flyingtitans.com>

WORKDIR /usr/local/src/zeffclient

COPY . /usr/local/src/zeffclient

RUN make install && \
 rm -f "/usr/local/lib/python3.7/site-packages/ZeffClient.egg-link"

CMD [ "bash" ]

