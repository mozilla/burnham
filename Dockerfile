FROM python:3.7-alpine as dist

LABEL maintainer "Raphael Pierzina <raphael@hackebrot.de>"

RUN apk add --no-cache --virtual \
    python3-dev \
    libffi-dev \
    build-base

COPY . /usr/src/burnham/
WORKDIR /usr/src/burnham

RUN python -m pip install --upgrade --no-cache-dir \
    pip \
    setuptools \
    wheel \
    pep517 \
    && python -m pep517.build . \
    && mv /usr/src/burnham/dist /dist

FROM python:3.7-alpine

LABEL maintainer "Raphael Pierzina <raphael@hackebrot.de>"

COPY --from=dist /dist/*.whl /tmp/dist/

RUN python -m venv venv
RUN source venv/bin/activate

RUN python -m pip install --upgrade pip
RUN python -m pip install /tmp/dist/*.whl

ENTRYPOINT [ "burnham" ]
