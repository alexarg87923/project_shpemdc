FROM python:3.12-alpine AS builder
WORKDIR /app

RUN python3 -m venv env
COPY ./requirements.txt ./
RUN ./env/bin/pip install -r requirements.txt

COPY ./static ./static
COPY ./templates ./templates
COPY ./helper.py .
COPY ./app.py .

CMD ["./env/bin/gunicorn", "-b", "0.0.0.0:8000", "app:app"]
EXPOSE 8000
