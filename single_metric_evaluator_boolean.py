import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Load Excel file
file_path = 'dataset_comparacion.xlsx'
df = pd.read_excel(file_path)

df = df[(df['Score_num'] != -1) & (df['Score_num'] != "VACIO")]

# Extract 'Score_num' and 'Relacion_spacy_jcn' columns
score_num = df['Score_num'].apply(lambda x: x if x != 'VACIO' else -1)
evaluation_binary = df['Eval_spacy_senses'].apply(lambda x: 1 if x else 0)
print(df['Eval_spacy_senses'])
print(evaluation_binary)


# Calculate the correlation coefficient
corr_coef = np.corrcoef(score_num, evaluation_binary)[0][1]

print("Correlation: ", corr_coef)

# Create a scatter plot
plt.scatter(evaluation_binary, score_num)

plt.xlabel('Relacion_spacy_jcn')
plt.ylabel('Score_num')
plt.title('Score_num vs Relacion_spacy_jcn')
plt.show()
