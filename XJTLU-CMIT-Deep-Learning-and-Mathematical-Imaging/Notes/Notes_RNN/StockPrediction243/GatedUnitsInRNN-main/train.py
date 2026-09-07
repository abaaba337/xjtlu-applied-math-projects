"""Chronological one-step stock prediction with the supplied teaching cells."""
import argparse
from pathlib import Path

import torch
from sklearn.preprocessing import MinMaxScaler

from datasets import get_data
from network import Network

HERE = Path(__file__).resolve().parent


@torch.no_grad()
def evaluate(model, data):
    model.eval()
    model.reset_hidden_state()
    predictions = torch.cat([model(row.reshape(1, 1))[0] for row in data[:-1]])
    loss = torch.nn.functional.mse_loss(predictions, data[1:]).item()
    model.reset_hidden_state()
    return loss, predictions


def train(data_file=HERE / "data/stock.csv", epochs=15, learning_rate=0.05,
          sequence_len=12, max_rows=None, seed=0):
    if epochs < 1 or learning_rate <= 0:
        raise ValueError("epochs and learning_rate must be positive.")
    torch.manual_seed(seed)
    train_values, test_values = get_data(data_file, sequence_len, 0.3, max_rows)
    scaler = MinMaxScaler(feature_range=(-1, 1))
    train_data = torch.tensor(scaler.fit_transform(train_values), dtype=torch.float32)
    test_data = torch.tensor(scaler.transform(test_values), dtype=torch.float32)
    model = Network(rnn_cell="lstm", sigmoid=False, rnn_units=2)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    for epoch in range(epochs):
        model.train()
        model.reset_hidden_state()
        total = 0.0
        # Truncated backpropagation bounds memory while retaining chronological state.
        for start in range(0, len(train_data) - 1, sequence_len):
            stop = min(start + sequence_len, len(train_data) - 1)
            predictions = torch.cat([model(row.reshape(1, 1))[0]
                                     for row in train_data[start:stop]])
            loss = torch.nn.functional.mse_loss(predictions, train_data[start + 1:stop + 1])
            if not torch.isfinite(loss):
                raise FloatingPointError("Non-finite training loss.")
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            model.rnn.h = model.rnn.h.detach()
            model.rnn.c_t = model.rnn.c_t.detach()
            total += loss.item() * (stop - start)
        validation_loss, _ = evaluate(model, test_data)
        scheduler.step()
        print(f"epoch={epoch + 1} train_mse={total / (len(train_data) - 1):.6f} "
              f"test_mse={validation_loss:.6f}")
    return model, scaler, validation_loss


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=HERE / "data/stock.csv")
    parser.add_argument("--epochs", type=int, default=15)
    parser.add_argument("--max-rows", type=int, help="Limit observations for a smoke run.")
    parser.add_argument("--output", type=Path, help="Optional new checkpoint path (must not exist).")
    args = parser.parse_args()
    model, scaler, loss = train(args.data, epochs=args.epochs, max_rows=args.max_rows)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("xb") as checkpoint:
            torch.save({"model_state_dict": model.state_dict(), "test_mse": loss,
                        "scaler_min": scaler.min_.tolist(), "scaler_scale": scaler.scale_.tolist()}, checkpoint)
