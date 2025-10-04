import requests
from fastapi import FastAPI
from pydantic import BaseModel

from .infer import load_model, run_inference

app = FastAPI()
model = load_model()

class InferenceRequest(BaseModel):
    face_url: str
    shape_url: str
    color_url: str | None = None

def fetch_bytes(url: str) -> bytes:
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.content

@app.post("/run")
def run(request: InferenceRequest):
    face_bytes = fetch_bytes(request.face_url)
    shape_bytes = fetch_bytes(request.shape_url)
    color_bytes = fetch_bytes(request.color_url) if request.color_url else None

    result_b64 = run_inference(model, face_bytes, shape_bytes, color_bytes)
    return {"output": result_b64}
