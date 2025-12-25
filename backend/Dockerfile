FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model (NO system deps needed)
RUN python -m spacy download en_core_web_sm

# Copy app code
COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app.wsgi:app"]

