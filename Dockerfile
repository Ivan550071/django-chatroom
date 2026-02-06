# Use official Python runtime as base image
FROM python:3.13-slim

# Set environment variables
# PYTHONUNBUFFERED ensures Python output is sent directly to logs
ENV PYTHONUNBUFFERED=1
# PYTHONDONTWRITEBYTECODE prevents creation of .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Set work directory in container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy entire project
COPY . /app/

# Expose port
EXPOSE 8000

# Run gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "chatroom.wsgi:application"]
