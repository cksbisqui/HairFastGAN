# ✅ CUDA-enabled base image (Ubuntu 22.04, cudnn8, runtime)
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# 🛠 Prevent tzdata from hanging during install
ENV DEBIAN_FRONTEND=noninteractive

# 🛠 Install Python 3.10 and system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 python3.10-dev python3.10-distutils \
    python3-pip build-essential cmake ninja-build git \
    libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev tzdata \
    && rm -rf /var/lib/apt/lists/*

# 🐍 Ensure python3 points to Python 3.10
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 2
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 2

# 🧠 Set CUDA environment variables
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=$CUDA_HOME/bin:$PATH
ENV LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

# 🐍 Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r /tmp/requirements.txt

# 📦 Copy your app code
COPY . /app
WORKDIR /app

# 🌐 Expose port
EXPOSE 8000

# 🚀 Start FastAPI server
CMD ["uvicorn", "app.serve:app", "--host", "0.0.0.0", "--port", "8000"]

