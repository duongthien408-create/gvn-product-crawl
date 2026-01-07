FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port (Railway uses PORT env var)
EXPOSE 8080

# Run with gunicorn
CMD gunicorn --bind 0.0.0.0:${PORT:-8080} --timeout 120 --workers 2 --threads 2 app:app
