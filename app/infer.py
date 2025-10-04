import io, base64, os
from pathlib import Path
from PIL import Image
import torch
from torchvision import transforms
import gdown  # lightweight downloader

from hair_swap import HairFast, get_parser

BASE_DIR = Path(__file__).parent.parent
WEIGHTS_DIR = BASE_DIR / "weights"
WEIGHTS_DIR.mkdir(exist_ok=True)

# Map of required weights and their download URLs (example: Google Drive or Hugging Face)
WEIGHTS_URLS = {
    "StyleGAN/ffhq.pth": "https://huggingface.co/chucks/hairfastgan-weights/resolve/main/StyleGAN/ffhq.pth",
    "PostProcess/rotate_best.pth": "https://huggingface.co/chucks/hairfastgan-weights/resolve/main/PostProcess/rotate_best.pth",
    "Blending/ffhq_G.pth": "https://huggingface.co/chucks/hairfastgan-weights/resolve/main/Blending/ffhq_G.pth",
    "PostProcess/pp_model.pth": "https://huggingface.co/chucks/hairfastgan-weights/resolve/main/PostProcess/pp_model.pth",
    "ShapeAdaptor/shape_predictor_68_face_landmarks.dat": "https://huggingface.co/chucks/hairfastgan-weights/resolve/main/ShapeAdaptor/shape_predictor_68_face_landmarks.dat"
}


def ensure_weights():
    for rel_path, url in WEIGHTS_URLS.items():
        dest = WEIGHTS_DIR / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists():
            print(f"Downloading {rel_path}...")
            gdown.download(url, str(dest), quiet=False)

def load_model():
    ensure_weights()
    parser = get_parser()
    args = parser.parse_args([])

    args.ckpt = str(WEIGHTS_DIR / "StyleGAN" / "ffhq.pth")
    args.rotate_checkpoint = str(WEIGHTS_DIR / "PostProcess" / "rotate_best.pth")
    args.blending_checkpoint = str(WEIGHTS_DIR / "Blending" / "ffhq_G.pth")
    args.pp_checkpoint = str(WEIGHTS_DIR / "PostProcess" / "pp_model.pth")

    args.device = "cuda" if torch.cuda.is_available() else "cpu"

    model = HairFast(args)
    model.eval()
    return model

def run_inference(model, face_bytes, shape_bytes, color_bytes=None):
    face_img = Image.open(io.BytesIO(face_bytes)).convert("RGB")
    shape_img = Image.open(io.BytesIO(shape_bytes)).convert("RGB")
    color_img = Image.open(io.BytesIO(color_bytes)).convert("RGB") if color_bytes else face_img

    with torch.no_grad():
        result_tensor = model.swap(face_img, shape_img, color_img)

    if isinstance(result_tensor, torch.Tensor):
        result_pil = transforms.ToPILImage()(result_tensor.squeeze().cpu())
    else:
        result_pil = result_tensor

    buf = io.BytesIO()
    result_pil.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")
