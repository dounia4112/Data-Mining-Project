import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from imblearn.under_sampling import RandomUnderSampler
from sklearn.metrics import confusion_matrix, roc_curve, auc
import time
import sys

# sys.path.insert(0, "../../../Data-Mining-Project")
sys.path.insert(0, "D:\\2M\D.Mining\Data-Mining-Project")
# from models.knn import KNNClassifier
from models.KNN import KNN
from src.utils import split_data, compute_metrics, plot_confusion_matrix

# ----------------------------------------------------------------#
# Load data
# ----------------------------------------------------------------#

df = pd.read_csv("../../data/interim/03_static_dataset_features_built.csv", index_col=0)

# ----------------------------------------------------------------#
# Split Data
# ----------------------------------------------------------------#
X_train, X_test, y_train, y_test = split_data(df)
X_train.shape, y_train.shape
# ----------------------------------------------------------------#
# Undersampling
# ----------------------------------------------------------------#
import numpy as np

desired_num_samples = 34
sampling_strategy_dict = {
    class_label: desired_num_samples
    for class_label, desired_num_samples in zip(*np.unique(y_train, return_counts=True))
}

# Apply random undersampling to the training data
undersampler = RandomUnderSampler(
    sampling_strategy=sampling_strategy_dict, random_state=42
)
X_resampled, y_resampled = undersampler.fit_resample(X_train, y_train)
X_resampled.shape, y_resampled.shape

# ----------------------------------------------------------------#
# Our KNN
# ----------------------------------------------------------------#
print("Our KNN with k = 5")
knn_3 = KNN(k=5)
# knn_3 = KNNClassifier(k=3, distance_metric="euclidean")

start_time = time.time()
knn_3.fit(X_resampled, y_resampled)
# knn_3.fit(X_train, y_train)
y_pred = knn_3.predict(X_test)
end_time = time.time()
RF_exec_time = end_time - start_time

compute_metrics(y_test, y_pred)
print("Execution Time: ", RF_exec_time)

cm = confusion_matrix(y_test, y_pred)

plot_confusion_matrix(cm)
# ----------------------------------------------------------------#
# SKLearn KNN
# ----------------------------------------------------------------#
print("SKLearn KNN with k = 5")
from sklearn.neighbors import KNeighborsClassifier
knn_sklearn = KNeighborsClassifier(n_neighbors=5)
knn_sklearn.fit(X_train, y_train)   
y_pred_sklearn = knn_sklearn.predict(X_test)
compute_metrics(y_test, y_pred_sklearn)