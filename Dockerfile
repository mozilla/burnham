FROM python:3.7-alpine as dist

LABEL maintainer "Raphael Pierzina <raphael@hackebrot.de>"

COPY . /usr/src/burnham/
WORKDIR /usr/src/burnham

RUN python -m pip install --upgrade --no-cache-dir pip wheel pep517 \
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
