# CUDA 11.8 devel (includes nvcc) on Ubuntu 22.04
FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

# Avoid interactive prompts (tzdata, etc.)
ENV DEBIAN_FRONTEND=noninteractive

# System deps: Python 3.10 + build toolchain for PyTorch extensions
RUN apt-get update && apt-get install -y \
    python3.10 python3.10-dev python3.10-distutils \
    python3-pip \
    build-essential gcc g++ make \
    cmake ninja-build git \
    libopenblas-dev liblapack-dev \
    libx11-dev libgtk-3-dev \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Ensure python3/pip point at 3.10
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 2 && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 2

# CUDA environment
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=$CUDA_HOME/bin:$PATH
ENV LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

# Recommended: restrict arch list to your GPU family to speed compilation and avoid mismatch
# RunPod often uses T4 (75), A10/A100 (86, 80). Your logs show compute_86, so we set 86 explicitly.
ENV TORCH_CUDA_ARCH_LIST="86"

# Upgrade packaging tools
RUN pip install --upgrade pip setuptools wheel

# Install Python deps first to leverage Docker layer caching
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Copy app code
COPY . /app
WORKDIR /app

# Precompile StyleGAN2 fused ops so they don’t JIT during server startup
# This imports the module that triggers torch.utils.cpp_extension.load() builds.
# If your import path differs, adjust accordingly.
RUN python3 - << 'PY'
import os
# Respect the arch list from env and ensure CUDA is visible
os.environ.setdefault("TORCH_CUDA_ARCH_LIST", "86")
# Import the fused op to trigger build
from models.stylegan2.op import fused_act
print("Precompiled fused_act successfully.")
PY

# Expose FastAPI port
EXPOSE 8000

# Start server
CMD ["uvicorn", "app.serve:app", "--host", "0.0.0.0", "--port", "8000"]
