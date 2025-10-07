# precompile.py
import os

# Ensure we only target the arch we want (your logs showed compute_86)
os.environ.setdefault("TORCH_CUDA_ARCH_LIST", "86")

print("Precompiling StyleGAN2 fused ops…")

# Import triggers torch.utils.cpp_extension.load() and builds the CUDA extension
from models.stylegan2.op import fused_act  # noqa: F401

print("✅ Precompiled fused_act successfully.")
