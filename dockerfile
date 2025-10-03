FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y python3 python3-pip git git-lfs && rm -rf /var/lib/apt/lists/*

# Clone HairFastGAN repo + weights
RUN git clone https://huggingface.co/AIRI-Institute/HairFastGAN /workspace/HairFastGAN && \
    cd /workspace/HairFastGAN && git lfs pull

WORKDIR /workspace/HairFastGAN

# Install dependencies
RUN pip install --upgrade pip
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121
RUN pip install fastapi uvicorn pillow
RUN pip install opencv-python scikit-image numpy

# Copy server files
COPY app /workspace/HairFastGAN/app

EXPOSE 8000
CMD ["uvicorn", "app.serve:app", "--host", "0.0.0.0", "--port", "8000"]
