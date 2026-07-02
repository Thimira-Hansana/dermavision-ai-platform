"""Albumentations pipelines."""

from __future__ import annotations

import albumentations as A
from albumentations.pytorch import ToTensorV2


def build_train_transforms(image_size: int) -> A.Compose:
    return A.Compose(
        [
            A.Resize(image_size, image_size),
            A.RandomRotate90(p=0.5),
            A.HorizontalFlip(p=0.5),
            A.VerticalFlip(p=0.2),
            A.ShiftScaleRotate(
                shift_limit=0.05,
                scale_limit=0.1,
                rotate_limit=25,
                border_mode=0,
                p=0.4,
            ),
            A.RandomBrightnessContrast(p=0.3),
            A.GaussianBlur(blur_limit=(3, 5), p=0.15),
            A.ElasticTransform(alpha=1.0, sigma=30.0, p=0.1),
            A.CoarseDropout(num_holes_range=(1, 3), hole_height_range=(0.05, 0.12), hole_width_range=(0.05, 0.12), p=0.15),
            A.Normalize(),
            ToTensorV2(),
        ]
    )


def build_eval_transforms(image_size: int) -> A.Compose:
    return A.Compose([A.Resize(image_size, image_size), A.Normalize(), ToTensorV2()])
