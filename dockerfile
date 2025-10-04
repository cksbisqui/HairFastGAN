FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip git git-lfs wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace/HairFastGAN

# Copy repo contents
COPY . /workspace/HairFastGAN

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install fastapi uvicorn

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "app.serve:app", "--host", "0.0.0.0", "--port", "8000"]
