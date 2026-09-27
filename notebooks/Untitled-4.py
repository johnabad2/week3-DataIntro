# Remove rows missing either variable before calculating correlations.
# Import libraries and give them short, conventional aliases.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Use a consistent style for all charts in this notebook.
sns.set_theme(style="whitegrid")

df = pd.read_csv("C:\\Users\\abadj\\Documents\\GitHub\\CSC1171\\Week 1\\week3-DataIntro\\data\\penguins.csv")
df.head(3)

# Build Anscombe's quartet as one table.
x = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
ys = {
    "I":   (x, [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]),
    "II":  (x, [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]),
    "III": (x, [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]),
    "IV":  ([8] * 7 + [19] + [8] * 3,
            [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]),
}
anscombe = pd.DataFrame(
    [(name, xi, yi) for name, (xs, yv) in ys.items() for xi, yi in zip(xs, yv)],
    columns=["dataset", "x", "y"],
)

# Calculate the same summaries that make the four datasets look similar.
summary = anscombe.groupby("dataset").agg(
    x_mean=("x", "mean"), y_mean=("y", "mean"),
    x_var=("x", "var"), y_var=("y", "var"),
)
summary["r"] = anscombe.groupby("dataset")[["x", "y"]].corr().xs("x", level=1)["y"]
print(summary.round(2))

sub = df.dropna(subset=["bill_length_mm", "bill_depth_mm"])

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

# Left: the overall relationship across all penguins.
# corr() uses Pearson correlation by default, so the line measures linear association.
sns.regplot(data=sub, x="bill_length_mm", y="bill_depth_mm",
            scatter_kws={"alpha": 0.6}, line_kws={"color": "black"}, ax=axes[0])
axes[0].set_title(f"All penguins (Pearson r = {sub['bill_length_mm'].corr(method='pearson', other=sub['bill_depth_mm']):.2f})")

# Right: draw one fitted line for each species.
for sp, g in sub.groupby("species"):
    sns.regplot(data=g, x="bill_length_mm", y="bill_depth_mm",
                scatter_kws={"alpha": 0.6}, label=sp, ax=axes[1])
axes[1].legend(title="species")
axes[1].set_title("By species: every slope flips")

plt.tight_layout()
plt.show()

print("overall: ", round(sub["bill_length_mm"].corr(method="pearson", other=sub["bill_depth_mm"]), 3))
for sp, g in sub.groupby("species"):
    print(f"{sp:12s}", round(g["bill_length_mm"].corr(method="pearson", other=g["bill_depth_mm"]), 3))