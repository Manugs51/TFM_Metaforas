import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ast
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


# Load Excel file
file_path = 'dataset_comparacion.xlsx'
df = pd.read_excel(file_path)

df = df[(df['Score_num'] != -1) & (df['Score_num'] != "VACIO")]

# Extract 'Score_num' and 'Relacion_spacy_jcn' columns
score_num = df['Score_num'].apply(lambda x: x if x != 'VACIO' else -1)
relacion_spacy_jcn = df['Relacion_spacy_jcn'].apply(lambda x: ast.literal_eval(x)[0])


# Calculate the correlation coefficient
corr_coef = np.corrcoef(score_num, relacion_spacy_jcn)[0][1]

print(corr_coef)

# Create a scatter plot
#plt.scatter(relacion_spacy_jcn, score_num)

#sns.set(style="darkgrid")
#sns.jointplot(x=relacion_spacy_jcn, y=score_num, kind="hex", color="blue")

plt.hexbin(relacion_spacy_jcn, score_num, gridsize=20, cmap='viridis')

plt.xlabel('Relacion_spacy_jcn')
plt.ylabel('Score_num')
plt.title('Score_num vs Relacion_spacy_jcn')
plt.colorbar(label='Density')
plt.show()


# Prepare data for k-fold cross-validation
X = relacion_spacy_jcn.values.reshape(-1, 1)
y = (score_num > 0).astype(int).to_numpy()  # Convert y to a NumPy array

# Initialize k-fold cross-validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Find the best threshold using k-fold cross-validation
best_threshold = 0
best_avg_accuracy = 0
best_avg_precision = 0
best_avg_recall = 0
best_avg_f1_score = 0

for threshold in range(0, 101, 1):
    threshold /= 100
    accuracies = []
    precisions = []
    recalls = []
    f1_scores = []
    
    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        
        y_pred_train = (X_train <= threshold).astype(int).flatten()
        accuracy = accuracy_score(y_train, y_pred_train)
        precision, recall, f1_score, _ = precision_recall_fscore_support(y_train, y_pred_train, average='binary')

        accuracies.append(accuracy)
        precisions.append(precision)
        recalls.append(recall)
        f1_scores.append(f1_score)
    
    avg_accuracy = np.mean(accuracies)
    avg_precision = np.mean(precisions)
    avg_recall = np.mean(recalls)
    avg_f1_score = np.mean(f1_scores)
    
    if avg_accuracy > best_avg_accuracy:
        best_avg_accuracy = avg_accuracy
        best_avg_precision = avg_precision
        best_avg_recall = avg_recall
        best_avg_f1_score = avg_f1_score
        best_threshold = threshold

print(f"Best threshold: {best_threshold}")
print(f"Average accuracy across 5 folds: {best_avg_accuracy}")
print(f"Average precision across 5 folds: {best_avg_precision}")
print(f"Average recall across 5 folds: {best_avg_recall}")
print(f"Average F1-score across 5 folds: {best_avg_f1_score}")
