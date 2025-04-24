FROM python:3.12-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install fastapi uvicorn

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 8081

# Command to run the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8081"] 