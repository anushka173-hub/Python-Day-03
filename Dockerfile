
# Use the official Python image
FROM python:3.14-slim

# Set the working directory
WORKDIR /app

# Copy dependency list
COPY requirements.txt .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Application port
EXPOSE 8000

# Start FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
