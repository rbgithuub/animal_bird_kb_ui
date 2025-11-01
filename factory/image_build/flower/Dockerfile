FROM python:3.11-slim

# Install Celery and Flower
RUN pip install --no-cache-dir celery flower

# Set working directory
WORKDIR /app

# Default command
CMD ["sh", "-c", "flower --broker=${CELERY_BROKER_URL} --address=0.0.0.0 --port=5555"]

