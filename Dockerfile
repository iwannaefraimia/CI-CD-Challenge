## Use an official Python runtime as a parent image
FROM python:3.9-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Use a smaller runtime image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application files
COPY . .

# Expose the port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]


