FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONPATH=/app

CMD ["python", "-m", "flower", "--broker=${CELERY_BROKER_URL}", "--address=0.0.0.0", "--port=5555"]
