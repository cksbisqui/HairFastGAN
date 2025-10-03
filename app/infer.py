import io, base64
from PIL import Image
from hairfast import hair_fast, init_model  # adapt to repo’s API

def load_model():
    return init_model()

def run_inference(model, face_bytes, shape_bytes, color_bytes=None):
    face_img = Image.open(io.BytesIO(face_bytes)).convert("RGB")
    shape_img = Image.open(io.BytesIO(shape_bytes)).convert("RGB")
    color_img = Image.open(io.BytesIO(color_bytes)).convert("RGB") if color_bytes else None

    result = hair_fast(model, face_img, shape_img, color_img)  # returns PIL Image
    buf = io.BytesIO()
    result.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")
