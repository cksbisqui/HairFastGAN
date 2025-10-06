import requests
from fastapi import FastAPI
from pydantic import BaseModel

from .infer import load_model, run_inference

app = FastAPI()

# Load model once at startup
print("🚀 Starting server…")
model = load_model()
print("✅ Model loaded and ready for inference")

class InferenceRequest(BaseModel):
    face_url: str
    shape_url: str
    color_url: str | None = None

def fetch_bytes(url: str) -> bytes:
    print(f"🌐 Fetching image from: {url}")
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.content

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run")
def run(request: InferenceRequest):
    print("📥 Inference request received")
    print(f"🖼️ face_url: {request.face_url}")
    print(f"🖼️ shape_url: {request.shape_url}")
    if request.color_url:
        print(f"🎨 color_url: {request.color_url}")

    face_bytes = fetch_bytes(request.face_url)
    shape_bytes = fetch_bytes(request.shape_url)
    color_bytes = fetch_bytes(request.color_url) if request.color_url else None

    print("⚙️ Running inference…")
    result_b64 = run_inference(model, face_bytes, shape_bytes, color_bytes)
    print("✅ Inference completed")

    return {"output": result_b64}