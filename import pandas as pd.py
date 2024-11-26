import pandas as pd
import numpy as np

# Input data
data = {
    "ID": ["BFW", "RKA", "QSQ", "WMZ"],
    "Performance": [-9.51, 40.53, -13.97, -43.68],
    "Environment": [6, 5, 8, 5],
    "Social": [1, 6, 8, 10],
    "Governance": [2, 1, 10, 7]
}
df = pd.DataFrame(data)

# Columns to include in the calculation
metrics = ["Performance", "Environment", "Social", "Governance"]

# Step 1: Normalize the data (0-1 range)
df_norm = df.copy()
for metric in metrics:
    max_val = df[metric].max()
    min_val = df[metric].min()
    df_norm[metric] = (df[metric] - min_val) / (max_val - min_val)

# Step 2: Calculate entropy
k = 1 / np.log(len(df))  # Constant for entropy calculation
entropy = []
for metric in metrics:
    p = df_norm[metric] / df_norm[metric].sum()  # Proportions
    entropy_metric = -k * (p * np.log(p + 1e-9)).sum()  # Avoid log(0)
    entropy.append(entropy_metric)

# Step 3: Calculate weights
entropy = np.array(entropy)
diversity = 1 - entropy  # Diversity degree
weights = diversity / diversity.sum()

# Step 4: Compute the combined score
scores = df_norm[metrics].values @ weights  # Matrix multiplication

# Add the combined score to the DataFrame
df["Combined Score"] = scores

# Output the result
print(df)
