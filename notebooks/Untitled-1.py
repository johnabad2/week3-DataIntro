# Import libraries and give them short, conventional aliases.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Use a consistent style for all charts in this notebook.
sns.set_theme(style="whitegrid")

df = pd.read_csv("C:\\Users\\abadj\\Documents\\GitHub\\CSC1171\\Week 1\\week3-DataIntro\\data\\penguins.csv")
df.head(3)

# Create one year of reproducible example data.
rng = np.random.default_rng(3)
dates = pd.date_range("2024-01-01", periods=365)
ts = pd.DataFrame({
    "date": dates,
    "station_a": 20 + 8 * np.sin(np.arange(365) / 58) + rng.normal(0, 1.4, 365),
    "station_b": 16 + 6 * np.sin(np.arange(365) / 58 + 0.7) + rng.normal(0, 1.4, 365),
})

fig, ax = plt.subplots(figsize=(11, 3.6))
ax.plot(ts["date"], ts["station_a"], label="Station A", lw=1)
ax.plot(ts["date"], ts["station_b"], label="Station B", lw=1)

# For each day, average Station A's value over a 14-day window.
# This uses the current day and the previous 13 days, reducing daily noise.
station_a_rolling_mean = ts["station_a"].rolling(14).mean()
ax.plot(
    ts["date"],
    station_a_rolling_mean,
    lw=2.5,
    color="black",
    label="Station A: 14-day rolling mean",
)

ax.set_ylabel("temperature (°C)")
ax.legend()
ax.set_title("Daily measurements and the longer-term trend")
plt.tight_layout()
plt.show()