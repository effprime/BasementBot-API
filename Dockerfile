
FROM python:3.7-alpine as builder

RUN apk update && \
    apk add --no-cache \
    gcc \
    musl-dev

WORKDIR /var/api
COPY Pipfile.lock .

RUN pip install pipenv && \
    pipenv requirements --dev > /tmp/requirements.txt && \
    pip install --no-cache-dir -r /tmp/requirements.txt

COPY . .

FROM python:3.7-alpine
WORKDIR /var/app
COPY --from=builder /usr/local /usr/local
COPY --from=builder /var/api .
CMD python3 -u app/main.py
