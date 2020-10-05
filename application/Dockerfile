FROM python:3.7-slim-buster as wheels

LABEL maintainer "Raphael Pierzina <raphael@hackebrot.de>"

COPY . /usr/src/burnham/
WORKDIR /usr/src/burnham

RUN python -m pip install --upgrade --no-cache-dir \
    pip>=20.1.1 \
    setuptools>=49.1.0 \
    wheel>=0.34.2
RUN python -m pip wheel -w /wheels -r requirements.txt
RUN python -m pip wheel -w /wheels .

FROM python:3.7-slim-buster

LABEL maintainer "Raphael Pierzina <raphael@hackebrot.de>"

COPY --from=wheels /wheels/*.whl /tmp/wheels/

RUN python -m venv venv
RUN . venv/bin/activate

RUN python -m pip install --upgrade pip
RUN python -m pip install /tmp/wheels/*.whl

ENTRYPOINT [ "burnham" ]
