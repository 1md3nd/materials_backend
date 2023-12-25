FROM python:3.11.7-alpine as build-stage

LABEL maintainer="1md3nd"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt

FROM python:3.11.7-alpine

LABEL maintainer="1md3nd"

ENV PYTHONUNBUFFERED 1

COPY --from=build-stage /py /py
COPY . /backend_server

WORKDIR /backend_server
EXPOSE 8000

RUN adduser --disabled-password --no-create-home app

ENV PATH = '/py/bin:$PATH'

CMD ["/py/bin/python","manage.py","runserver","0.0.0.0:8000"]