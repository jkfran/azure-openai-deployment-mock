FROM python:3.12-slim

# Install system dependencies and pip
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the mock API script
COPY ./mock_api.py /srv/mock_api.py

# Set working directory
WORKDIR /srv

# Expose the port for the API
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "mock_api:app", "--host", "0.0.0.0", "--port", "8000"]
