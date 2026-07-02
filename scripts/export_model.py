"""Model export entry point."""

from __future__ import annotations

from pathlib import Path

import torch

from dermavision_ai.core.constants import CLASS_ORDER
from dermavision_ai.core.settings import get_settings
from dermavision_ai.models.model_factory import build_model, load_checkpoint


def main() -> None:
    settings = get_settings()
    checkpoints = sorted(settings.model_dir.glob("*.pt"))
    if not checkpoints:
        raise FileNotFoundError("No checkpoint available for export.")
    checkpoint = checkpoints[-1]
    model = build_model(settings.default_model, num_classes=len(CLASS_ORDER), pretrained=False)
    load_checkpoint(model, checkpoint)
    model.eval()
    dummy = torch.randn(1, 3, 224, 224)
    torchscript_path = Path("models/checkpoints/model.torchscript")
    onnx_path = Path("models/checkpoints/model.onnx")
    traced = torch.jit.trace(model, dummy)
    traced.save(torchscript_path)
    torch.onnx.export(model, dummy, onnx_path, opset_version=17, input_names=["image"], output_names=["logits"])
    print({"torchscript": str(torchscript_path), "onnx": str(onnx_path)})


if __name__ == "__main__":
    main()
