# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a directory for the app
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    libpq-dev \
    build-essential \
    libssl-dev \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project files to the app directory
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Copy Nginx config file
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 8000 to the outside world
EXPOSE 8000

# Run the application
CMD ["sh", "-c", "nginx -g 'daemon off;' & gunicorn mon_projet.wsgi:application --bind 0.0.0.0:8000"]
