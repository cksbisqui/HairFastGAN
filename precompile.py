import os
import torch

# Only attempt if CUDA is available
if torch.cuda.is_available():
    # Detect GPU arch dynamically
    major, minor = torch.cuda.get_device_capability(0)
    arch = f"{major}{minor}"
    os.environ["TORCH_CUDA_ARCH_LIST"] = arch
    print(f"Precompiling StyleGAN2 fused ops for arch {arch}…")

    from models.stylegan2.op import fused_act  # noqa: F401

    print("✅ Precompiled fused_act successfully.")
else:
    print("⚠️ CUDA not available at build time, skipping fused op precompile.")
