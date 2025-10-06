# ✅ CUDA-enabled base image with dev tools
FROM nvidia/cuda:11.8.0-devel-ubuntu20.04

# 🛠 Install Python and system dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev \
    build-essential cmake ninja-build git \
    libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

# 🧠 Set CUDA environment variables
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=$CUDA_HOME/bin:$PATH
ENV LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

# 🐍 Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install fastapi uvicorn

# 📦 Copy your app code
COPY . /app
WORKDIR /app

# 🌐 Expose port
EXPOSE 8000

# 🚀 Start FastAPI server
CMD ["uvicorn", "app.serve:app", "--host", "0.0.0.0", "--port", "8000"]
