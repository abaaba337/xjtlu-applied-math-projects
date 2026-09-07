import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


if __name__ == "__main__":
    data_file = Path(__file__).resolve().parent / "data/stock.csv"
    data = pd.read_csv(data_file, header=0).dropna()
    data = data.sort_values('Date').reset_index(drop=True)

    price_high = data['High'].values
    price_low = data['Low'].values
    price_mid = (price_high + price_low) / 2.0

    fig, ax = plt.subplots(figsize=(20, 5))
    ax.grid(color='gray', linestyle='--')

    ax.plot(price_high, color='orange')
    ax.plot(price_low, color='blue')
    ax.plot(price_mid, color='black')

    print(len(price_mid))
    plt.xticks(range(0, data.shape[0], 500), data['Date'].loc[::500], rotation=45)
    plt.show()
