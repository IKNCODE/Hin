FROM python:3.12.4

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . .

WORKDIR /app/src

ENV DB_HOST=host.docker.internal
ENV DB_PORT=5432
ENV DB_NAME=history_in
ENV DB_USER=postgres
ENV DB_PASS=123


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]