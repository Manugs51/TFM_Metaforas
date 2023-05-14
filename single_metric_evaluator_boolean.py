import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report

# Load Excel file
file_path = 'dataset_comparacion.xlsx'
df = pd.read_excel(file_path)

df = df[(df['Score_num'] != -1) & (df['Score_num'] != "VACIO")]

# Extract 'Score_num' and 'Relacion_spacy_jcn' columns
score_num = df['Score_num'].apply(lambda x: x if x != 'VACIO' else -1)
evaluation_binary = df['Eval_spacy_senses'].apply(lambda x: 1 if x else 0)
score_num_binary = (score_num > 0).astype(int)

# Calculate the correlation coefficient
corr_coef = np.corrcoef(score_num, evaluation_binary)[0][1]

print("Correlation: ", corr_coef)

# Compute classification metrics
accuracy = accuracy_score(score_num_binary, evaluation_binary)
print("Accuracy: ", accuracy)

classification_rep = classification_report(score_num_binary, evaluation_binary)
print("Classification report: \n", classification_rep)

# Create a scatter plot
plt.scatter(evaluation_binary, score_num_binary)
plt.xlabel('Eval_spacy_senses')
plt.ylabel('Score_num > 0')
plt.title('Score_num > 0 vs Eval_spacy_senses')
plt.show()
