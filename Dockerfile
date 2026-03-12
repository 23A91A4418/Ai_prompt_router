# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies (if any were needed, but generativeai is pure python)
# RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --default-timeout=1000 -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Ensure the log file exists so we can mount it or just have it there
RUN touch route_log.jsonl

# Run main.py when the container launches
CMD ["python", "main.py"]
