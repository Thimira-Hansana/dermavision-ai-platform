# Troubleshooting

- If the dataset is not found, verify the HAM10000 files are under `data/` or `data/archive/`.
- If inference returns demo mode, train a model or point `DERMAVISION_MODEL_CHECKPOINT` to a saved `.pt` artifact.
- If Grad-CAM fails on a non-convolutional backbone, switch to a convolutional model such as EfficientNet or ResNet.
