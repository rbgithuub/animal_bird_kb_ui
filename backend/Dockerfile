# Use Python base image compatible with arm64
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies including uvicorn
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy backend code
COPY . .

# Expose port
EXPOSE 5000

# Run backend using uvicorn
CMD ["gunicorn", "app.main:app", "--bind", "0.0.0.0:5000"]
