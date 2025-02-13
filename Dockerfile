FROM python:3.14.0a5-alpine3.21 AS builder
WORKDIR /app

RUN python3 -m venv env
RUN source ./env/bin/activate
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./static ./static
COPY ./templates ./templates
COPY ./.env .
COPY ./helper.py .
COPY ./app.py .

CMD ["gunicorn", "-b", "0.0.0.0", "app:app"]
EXPOSE 8000
