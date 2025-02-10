# Dockerfile

# Use an official Python runtime as the base image
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama (Assuming Linux x86_64 architecture)
RUN curl -o ollama.deb https://ollama.ai/downloads/ollama-cli-linux-amd64.deb && \
    dpkg -i ollama.deb && \
    rm ollama.deb

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose ports for FastAPI (8000) and NiceGUI (8001)
EXPOSE 8000 8001

# Start the Ollama server and the application
CMD ["bash", "-c", "ollama serve & uvicorn main:app --host 0.0.0.0 --port 8000 & python gui.py"]
