FROM python:3.12-slim

WORKDIR /app

ENV FLASK_APP=app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod -R 755 /app

CMD ["flask", "run", "--host=0.0.0.0"]