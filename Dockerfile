
FROM python:3.7-alpine as builder

COPY Pipfile* /tmp/

RUN apk update && \
    apk add --no-cache \
    gcc \
    musl-dev

RUN pip install pipenv && \
    cd /tmp && pipenv lock --requirements > requirements.txt && \
    pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /var/api
COPY . .

FROM python:3.7-alpine
WORKDIR /var/app
COPY --from=builder /usr/local /usr/local
COPY --from=builder /var/api .
CMD python3 -u app/main.py
