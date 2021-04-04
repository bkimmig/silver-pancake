# TODO - user lighter weight image
FROM python:3.7-stretch as python

ENV PYTHONPATH="/src/:${PYTHONPATH}"

WORKDIR /src

COPY python/src/svc/requirements.txt /src/svc/requirements.txt
RUN pip install --no-cache-dir -r /src/svc/requirements.txt

COPY python/src/svc/ /src/svc/

