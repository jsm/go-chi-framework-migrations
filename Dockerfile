FROM python:3-alpine

RUN apk add --update --no-cache \
    build-base \
    netcat-openbsd \
    postgresql-dev \
    postgresql-client

COPY requirements.txt /src/requirements.txt
RUN pip install --upgrade pip
RUN cd /src && pip install -r requirements.txt

COPY . /src

EXPOSE 5000

WORKDIR /src

ENTRYPOINT ["./migrate_db.sh"]
