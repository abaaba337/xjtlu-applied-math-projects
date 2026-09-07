"""Shared DRIVE loading for the lecture and exercise notebooks."""
import os
from pathlib import Path

from PIL import Image
import torch
from torchvision.transforms.functional import to_tensor


def get_paths(base_path=None):
    root = Path(base_path or os.environ.get(
        "CMIT_DRIVE_DIR", Path(__file__).parent / "Notes/Notes_IMProcess/DRIVE"
    ))

    def locate(folder, number, suffix, extensions):
        candidates = {folder / f"{number:{padding}}_{suffix}.{ext}"
                      for padding in ("d", "02d") for ext in extensions}
        matches = sorted(path for path in candidates if path.is_file())
        if len(matches) != 1:
            raise FileNotFoundError(
                f"Expected one {suffix} file for DRIVE ID {number} in {folder}; "
                "set CMIT_DRIVE_DIR to the complete DRIVE dataset."
            )
        return matches[0]

    result = []
    for split, numbers in (("training", range(21, 41)), ("test", range(1, 21))):
        images = [locate(root / split / "images", i, split, ("tif", "png"))
                  for i in numbers]
        masks = [locate(root / split / "1st_manual", i, "manual1", ("gif",))
                 for i in numbers]
        result.append([images, masks])
    return tuple(result)


class SegmentationDataset(torch.utils.data.Dataset):
    def __init__(self, paths, size=(256, 256)):
        self.im_paths, self.gt_paths = paths
        if len(self.im_paths) != len(self.gt_paths):
            raise ValueError("Each image must have one ground-truth mask.")
        self.size = size

    def __len__(self):
        return len(self.im_paths)

    def __getitem__(self, index):
        with Image.open(self.im_paths[index]) as source:
            image = to_tensor(source.convert("RGB").resize(self.size, Image.Resampling.BILINEAR))
        with Image.open(self.gt_paths[index]) as source:
            mask = to_tensor(source.convert("L").resize(self.size, Image.Resampling.NEAREST))
        return image, (mask > 0.5).float()
