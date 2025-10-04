# Start from a Python base image
FROM python:3.10-slim

# Install system dependencies required for dlib and scientific libs
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install fastapi uvicorn

# Copy your app code
COPY . /app
WORKDIR /app

# Expose port
EXPOSE 8000

# Start the server
CMD ["uvicorn", "app.serve:app", "--host", "0.0.0.0", "--port", "8000"]

