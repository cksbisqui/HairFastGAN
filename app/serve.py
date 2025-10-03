from fastapi import FastAPI, UploadFile, File
from app.infer import load_model, run_inference

app = FastAPI()
model = load_model()

@app.post("/tryon")
async def try_on(face: UploadFile = File(...),
                 shape: UploadFile = File(...),
                 color: UploadFile = File(None)):
    face_bytes = await face.read()
    shape_bytes = await shape.read()
    color_bytes = await (color.read() if color else b"")
    output_png = run_inference(model, face_bytes, shape_bytes, color_bytes)
    return {"image_base64": output_png}
