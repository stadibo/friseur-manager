FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY requirements.txt .

RUN \
  apk update && \
  apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev libffi-dev sqlite && \
  python3 -m pip install -r requirements.txt --no-cache-dir && \
  apk --purge del .build-deps

COPY . .
EXPOSE 5000
CMD ["python3", "run.py"]