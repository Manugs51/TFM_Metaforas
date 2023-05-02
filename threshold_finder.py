import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Load Excel file
file_path = 'dataset_comparacion.xlsx'
df = pd.read_excel(file_path)

df = df[(df['Score_num'] != -1) & (df['Score_num'] != "VACIO")]

# Extract 'Score_num' and 'Relacion_spacy_jcn' columns
score_num = df['Score_num'].apply(lambda x: x if x != 'VACIO' else -1)
relacion_spacy_jcn = df['Relacion_spacy_jcn'].apply(lambda x: ast.literal_eval(x)[0])


# Create a scatter plot
plt.scatter(relacion_spacy_jcn, score_num)
plt.xlabel('Relacion_spacy_jcn')
plt.ylabel('Score_num')
plt.title('Score_num vs Relacion_spacy_jcn')
plt.show()


# Prepare data for training and testing
X_train, X_test, y_train, y_test = train_test_split(relacion_spacy_jcn.values.reshape(-1, 1), (score_num > 0).astype(int), test_size=0.2, random_state=42)

# Find the best threshold
best_threshold = 0
best_accuracy = 0

for threshold in range(0, 101, 1):
    threshold /= 100
    y_pred_train = (X_train <= threshold).astype(int).flatten()
    accuracy = accuracy_score(y_train, y_pred_train)
    
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_threshold = threshold

# Evaluate the classifier on the test set
y_pred_test = (X_test <= best_threshold).astype(int).flatten()
test_accuracy = accuracy_score(y_test, y_pred_test)

print(f"Best threshold: {best_threshold}")
print(f"Test accuracy: {test_accuracy}")
print(classification_report(y_test, y_pred_test))
