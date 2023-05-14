import numpy as np
import pandas as pd
import ast
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn import svm
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_recall_fscore_support
import pickle
from sklearn.naive_bayes import GaussianNB

from sklearn.neighbors import KNeighborsClassifier

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

def unpack_single_float_list(value):
    return ast.literal_eval(value)[0] if ast.literal_eval(value)[0] < 20 else 20

data = pd.read_excel("dataset_comparacion.xlsx")

data = data[(data['Score_num'] != -1) & (data['Score_num'] != "VACIO")]

feature_columns = ["Relacion_spacy_jcn", "Relacion_spacy_lch", "Relacion_spacy_li", "Relacion_spacy_lin", "Relacion_spacy_path", "Relacion_spacy_res", "Relacion_spacy_wpath", "Relacion_spacy_wup"]
X = data[feature_columns]  # Feature columns
y = data["Score_num"]  # Target column

# Convert list of single float to single float
X = X.applymap(unpack_single_float_list)
y = y.apply(lambda x: 1 if x > 0 else 0)

# Set up k-fold cross-validation with k=5
k = 5
skf = StratifiedKFold(n_splits=k, random_state=42, shuffle=True)

# Initialize metrics
accuracy_scores = []
precision_scores = []
recall_scores = []
fscore_scores = []

# Define the model
model = Sequential()
model.add(Dense(32, input_dim=len(feature_columns), activation='relu'))  # Hidden layer
model.add(Dense(16, activation='relu'))  # Hidden layer 2
model.add(Dense(1, activation='sigmoid'))  # Output layer

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy', 'Precision', 'Recall'])

# Loop through the k-folds
for train_index, test_index in skf.split(X, y):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    # Create and train the Random Forest classifier
    

     # Fit the model
    model.fit(X_train, y_train, epochs=100, batch_size=10, verbose=0)

    # Evaluate the model
    scores = model.evaluate(X_test, y_test, verbose=0)
    accuracy_scores.append(scores[1])
    precision_scores.append(scores[2])
    recall_scores.append(scores[3])

    # Calculate and store the accuracy and other metrics
    #accuracy = accuracy_score(y_test, y_pred)
    #accuracy_scores.append(accuracy)
    #precision, recall, fscore, _ = precision_recall_fscore_support(y_test, y_pred, average="weighted")
    #fscore_scores.append(fscore)

# Calculate and display the average accuracy and other metrics
avg_accuracy = np.mean(accuracy_scores)
avg_precision = np.mean(precision_scores)
avg_recall = np.mean(recall_scores)
avg_fscore = np.mean(fscore_scores)
print(f"Average Accuracy: {avg_accuracy * 100:.2f}%")
print(f"Average Precision: {avg_precision * 100:.2f}%")
print(f"Average Recall: {avg_recall * 100:.2f}%")
print(f"Average F-score: {avg_fscore * 100:.2f}%")

# Save the model
model.save('classifiersematchNN.h5')  
