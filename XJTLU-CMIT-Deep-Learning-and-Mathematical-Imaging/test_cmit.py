import json
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np
import pandas as pd
from PIL import Image
import torch
from sklearn.preprocessing import StandardScaler

from cmit_utils import SegmentationDataset, get_paths

ROOT = Path(__file__).resolve().parent
STOCK = ROOT / "Notes/Notes_RNN/StockPrediction243/GatedUnitsInRNN-main"
sys.path.insert(0, str(STOCK))
from datasets import get_data
from network import Network
from train import evaluate, train


def cell_source(notebook, marker):
    cells = json.loads((ROOT / notebook).read_text(encoding="utf-8"))["cells"]
    return next("".join(c["source"]) for c in cells
                if c["cell_type"] == "code" and marker in "".join(c["source"]))


class CMITRegression(unittest.TestCase):
    def test_stock_split_and_two_epoch_training(self):
        values, holdout = get_data(STOCK / "data/stock.csv", test_size=0.3, max_rows=48)
        self.assertEqual((len(values), len(holdout)), (33, 15))
        raw = pd.read_csv(STOCK / "data/stock.csv").dropna().sort_values("Date").iloc[:48]
        np.testing.assert_allclose(values[:, 0], ((raw.High + raw.Low) / 2).iloc[:33])
        np.testing.assert_allclose(holdout[:, 0], ((raw.High + raw.Low) / 2).iloc[33:])
        model, scaler, loss = train(epochs=2, max_rows=48)
        np.testing.assert_allclose(scaler.data_max_, values.max(axis=0))
        self.assertTrue(np.isfinite(loss))
        data = torch.tensor(scaler.transform(holdout), dtype=torch.float32)
        first = evaluate(model, data)[1]
        second = evaluate(model, data)[1]
        torch.testing.assert_close(first, second)
        self.assertFalse(first.requires_grad)
        for cell in ("gru", "lstm"):
            model = Network(rnn_cell=cell, sigmoid=True).double()
            model.reset_hidden_state()
            y, _ = model(torch.ones(1, 1, dtype=torch.float64))
            self.assertTrue(((0 <= y) & (y <= 1)).all())

    def test_masks_use_nearest_and_drive_ids_are_padded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mask = np.array([[0, 255], [255, 0]], dtype=np.uint8)
            Image.fromarray(mask).save(root / "mask.png")
            Image.new("RGB", (2, 2)).save(root / "image.png")
            image, label = SegmentationDataset([[root / "image.png"], [root / "mask.png"]], size=(5, 5))[0]
            expected = np.array(Image.fromarray(mask).resize((5, 5), Image.Resampling.NEAREST)) > 127
            np.testing.assert_array_equal(label[0].numpy(), expected)
            self.assertEqual(tuple(image.shape), (3, 5, 5))
            for split, numbers in (("training", range(21, 41)), ("test", range(1, 21))):
                for folder in ("images", "1st_manual"):
                    (root / split / folder).mkdir(parents=True)
                for i in numbers:
                    (root / split / "images" / f"{i:02d}_{split}.tif").touch()
                    (root / split / "1st_manual" / f"{i:02d}_manual1.gif").touch()
            training, testing = get_paths(root)
            self.assertEqual((len(training[0]), len(testing[0])), (20, 20))
            self.assertEqual(testing[0][0].name, "01_test.tif")

    def test_notebook_scaler_uses_only_training_rows_and_batch_one_survives(self):
        # Execute the actual preprocessing cell with a synthetic held-out price jump.
        notebook = "Notes/CMIT Lecture Notes.ipynb"
        frame = pd.DataFrame({k: np.arange(50, dtype=float) for k in
                              ("Open", "High", "Low", "Close", "Volume")})
        frame.loc[45:, ["Open", "High", "Low", "Close"]] += 1000
        frame["Date"] = pd.date_range("2020-01-01", periods=50)
        from unittest.mock import patch
        ns = {"pd": pd, "np": np, "StandardScaler": StandardScaler,
              "torch": torch, "nn": torch.nn}
        with patch.object(pd, "read_csv", return_value=frame.copy()):
            exec(cell_source(notebook, "ori_data = pd.read_csv"), ns)
        end = ns["split_index"] + ns["sequence_len"] - 1
        self.assertAlmostEqual(ns["scaler"].mean_[0], frame.Open.iloc[:end].mean())
        exec(cell_source(notebook, "class LSTMFNN("), ns)
        self.assertEqual(tuple(ns["LSTMFNN"]()(torch.zeros(1, 10, 5)).shape), (1,))

    def test_supplied_segmentation_and_denoising_weights_match(self):
        notebook = "Notes/CMIT Lecture Notes.ipynb"
        cells = json.loads((ROOT / notebook).read_text(encoding="utf-8"))["cells"]
        sources = ["".join(c["source"]) for c in cells if "class CNN(" in "".join(c["source"])]
        for source, filename, channels, size in [
            (sources[-2], "Notes323CNN.pth", 3, 256),
            (sources[-1], "Notes332Denoising.pth", 1, 28),
        ]:
            ns = {"nn": torch.nn, "torch": torch}
            exec(source, ns)
            model = ns["CNN"](img_size=size, in_channels=channels, out_channels=1)
            model.load_state_dict(torch.load(ROOT / "Notes/Notes_IMProcess" / filename,
                                            weights_only=True, map_location="cpu"))


if __name__ == "__main__":
    unittest.main()
