FROM python:3.9.10-alpine3.15

WORKDIR /flask

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN rm requirements.txt

COPY src .
ENTRYPOINT [ "python3", "/flask/server.py" ]
