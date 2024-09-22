FROM python:3.12.4

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . .

ENV DB_HOST = localhost
ENV DB_PORT = 5432
ENV DB_NAME = history_in
ENV DB_USER = postgres
ENV DB_PASS = 123

EXPOSE 8000

CMD ["cd", "src"]
CMD ["uvicorn", "main:app"]