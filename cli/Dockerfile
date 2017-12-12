FROM python:3-slim

WORKDIR /app

ADD . /app

RUN pip install --trusted-host pypi.python.org .

ENV DEBUG False

ENTRYPOINT ["osn-cli"]
