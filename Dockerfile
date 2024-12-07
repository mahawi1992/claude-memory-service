# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose the port
EXPOSE 8283

# Start command
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8283"]