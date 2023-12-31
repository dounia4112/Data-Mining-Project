import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

sys.path.insert(0,"D:\\2M\D.Mining\Data-Mining-Project")
from models.DBScan import DBScan
from src.utils import split_data, compute_metrics, plot_confusion_matrix, silhouette_score

# ----------------------------------------------------------------
# Load data
# ----------------------------------------------------------------
df = pd.read_csv("../../data/interim/03_static_dataset_features_built.csv", index_col=0)

# ----------------------------------------------------------------
# Data
# ----------------------------------------------------------------
X, y = df.drop(columns=["Fertility"]).values, df["Fertility"].values

# ----------------------------------------------------------------
# Hyperparameters tuning for dbscan
# ----------------------------------------------------------------

eps_range = np.arange(0.1, 1.0, 0.1)
min_samples_range = range(2, 10)
silhouette_scores = []

for eps in eps_range:
    for min_samples in min_samples_range:
        dbscan = DBScan(eps=eps, min_samples=min_samples)
        dbscan.fit(X)
        labels = dbscan.cluster_labels
        silhouette_avg = silhouette_score(X, labels)
        silhouette_scores.append(silhouette_avg)

# Reshape the silhouette_scores to match the shape of the heatmap
silhouette_scores = np.array(silhouette_scores).reshape(len(eps_range), len(min_samples_range))

# Create a heatmap
plt.figure(figsize=(10, 6))
eps_labels = [f"{eps:.1f}" for eps in eps_range]
min_samples_labels = [str(min_samples) for min_samples in min_samples_range]
plt.imshow(silhouette_scores, cmap='viridis', origin='lower', extent=[min_samples_range[0]-0.5, min_samples_range[-1]+0.5, eps_range[0]-0.05, eps_range[-1]+0.05])
plt.colorbar(label='Silhouette Score')
plt.xticks(min_samples_range, min_samples_labels)
plt.yticks(eps_range, eps_labels)
plt.xlabel('Min Samples')
plt.ylabel('Eps')
plt.title('Silhouette Score Heatmap for Different Eps and Min Samples')

# make the hitmap wider in the y axis
plt.gca().set_aspect('auto')
# Find the hyperparameters that give the maximum silhouette score in the plot
max_idx = np.unravel_index(np.argmax(silhouette_scores, axis=None), silhouette_scores.shape)
plt.scatter(min_samples_range[max_idx[1]], eps_range[max_idx[0]], marker='*', color='red', label=f'Maximum Silhouette Score: eps={eps_range[max_idx[0]]:.1f}, min_samples={min_samples_range[max_idx[1]]}')
# display the best hyperparameters in the plot
plt.legend()
plt.savefig('../../reports/figures/Part_2/DBScan_hyperparameters_tuning.png')
plt.show()
# save the plot
print(f"The following hyperparameters give the maximum silhouette score: eps={eps_range[max_idx[0]]:.1f}, min_samples={min_samples_range[max_idx[1]]}")

# print the number of clusters
print(f"Number of clusters: {len(np.unique(dbscan.cluster_labels))}")

# ----------------------------------------------------------------
# Train DBscan with the best hyperparameters
# ----------------------------------------------------------------
eps = 0.9
min_samples = 2
dbscan = DBScan(eps=eps, min_samples=min_samples)
dbscan.fit(X)
labels = dbscan.cluster_labels
# print the number of clusters
print(f"Number of clusters: {len(np.unique(labels))}")

# compute the silhouette score
silhouette_avg = silhouette_score(X, labels)