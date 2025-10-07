import os

# Match your GPU arch (86 for A10/A100, 75 for T4)
os.environ.setdefault("TORCH_CUDA_ARCH_LIST", "86")

print("Precompiling StyleGAN2 fused ops…")

from models.stylegan2.op import fused_act  # noqa: F401

print("✅ Precompiled fused_act successfully.")

