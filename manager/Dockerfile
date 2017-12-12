FROM python:3-slim

WORKDIR /app

ADD . /app

RUN pip install --trusted-host pypi.python.org .

EXPOSE 80

ENV DEBUG False

CMD ["osn-manager", "[::]:80"]
