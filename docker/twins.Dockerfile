FROM python:3.7-stretch as python

ENV PYTHONPATH="/src/:${PYTHONPATH}"

WORKDIR /src

RUN pip install jupyterlab==3.0.12

# TODO - change this around... but due to caching this makes the builds faster
COPY python/src/twins/requirements.txt /src/twins/requirements.txt
RUN pip install --no-cache-dir -r /src/twins/requirements.txt

COPY python/src/twins /src/twins
COPY python/src/twins /src/svc

