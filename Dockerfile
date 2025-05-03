# Dockerfile

FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Flask runs on port 5000
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
