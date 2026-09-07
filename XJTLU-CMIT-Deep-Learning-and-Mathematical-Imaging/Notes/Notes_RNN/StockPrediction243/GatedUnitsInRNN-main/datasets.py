import numpy as np
import pandas as pd


def get_data(data_file, sequence_len=12, test_size=0.4, max_rows=None):
    if sequence_len < 1 or not 0 < test_size < 1:
        raise ValueError("Require sequence_len >= 1 and 0 < test_size < 1.")
    data = pd.read_csv(data_file, usecols=["Date", "High", "Low"]).dropna()
    data["Date"] = pd.to_datetime(data["Date"], errors="raise")
    data = data.sort_values("Date")
    if data["Date"].duplicated().any():
        raise ValueError("Stock dates must be unique.")
    if max_rows is not None:
        if max_rows < 1:
            raise ValueError("max_rows must be positive.")
        data = data.iloc[:max_rows]
    prices = ((data["High"] + data["Low"]) / 2).to_numpy(dtype=float)
    if not np.isfinite(prices).all():
        raise ValueError("Stock prices must be finite.")
    prices = prices[:len(prices) // sequence_len * sequence_len].reshape(-1, 1)
    split = int(len(prices) * (1 - test_size))
    if split < 2 or len(prices) - split < 2:
        raise ValueError("Need at least two observations in each chronological split.")
    return prices[:split], prices[split:]
