FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create static directory
RUN mkdir -p /app/static

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create static directory in the project root
RUN mkdir -p static

# Expose ports for different services
EXPOSE 8000 8001 8002 8003

# Command to run the application (this will be overridden by docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 