FROM python:3.7-alpine

LABEL maintainer "Raphael Pierzina <raphael@hackebrot.de>"

RUN adduser -D fake-data-platform
WORKDIR /home/fake-data-platform

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -U pip
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app.py app.py

ENV FLASK_APP app.py

COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

RUN chown -R fake-data-platform:fake-data-platform ./
USER fake-data-platform

EXPOSE 5000
ENTRYPOINT [ "./entrypoint.sh" ]
