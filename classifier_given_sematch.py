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

# Loop through the k-folds
for train_index, test_index in skf.split(X, y):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    # Create and train the Random Forest classifier
    #clf = RandomForestClassifier(n_estimators=1000, random_state=42)
    '''
    Average Accuracy: 60.58%
    Average Precision: 61.95%
    Average Recall: 60.58%
    Average F-score: 52.25%
    '''
    #clf = svm.SVC(kernel='linear')
    '''
    Average Accuracy: 59.30%
    Average Precision: 66.51%
    Average Recall: 59.30%
    Average F-score: 45.71%
    '''
    #clf = GradientBoostingClassifier(n_estimators=1000, learning_rate=1.0, max_depth=1, random_state=42)
    '''
    Average Accuracy: 59.73%
    Average Precision: 59.14%
    Average Recall: 59.73%
    Average F-score: 51.75%
    '''
    #clf = KNeighborsClassifier(n_neighbors=5)
    '''
    Average Accuracy: 53.14%
    Average Precision: 60.53%
    Average Recall: 53.14%
    Average F-score: 48.98%
    '''
    #clf = LogisticRegression(random_state=42)
    '''
    Average Accuracy: 59.30%
    Average Precision: 62.28%
    Average Recall: 59.30%
    Average F-score: 46.38%
    '''
    clf = GaussianNB()
    '''
    Average Accuracy: 57.17%
    Average Precision: 53.86%
    Average Recall: 57.17%
    Average F-score: 49.33%
    '''
    clf.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = clf.predict(X_test)

    # Calculate and store the accuracy and other metrics
    accuracy = accuracy_score(y_test, y_pred)
    accuracy_scores.append(accuracy)
    precision, recall, fscore, _ = precision_recall_fscore_support(y_test, y_pred, average="weighted")
    precision_scores.append(precision)
    recall_scores.append(recall)
    fscore_scores.append(fscore)

# Calculate and display the average accuracy and other metrics
avg_accuracy = np.mean(accuracy_scores)
avg_precision = np.mean(precision_scores)
avg_recall = np.mean(recall_scores)
avg_fscore = np.mean(fscore_scores)
print(f"Average Accuracy: {avg_accuracy * 100:.2f}%")
print(f"Average Precision: {avg_precision * 100:.2f}%")
print(f"Average Recall: {avg_recall * 100:.2f}%")
print(f"Average F-score: {avg_fscore * 100:.2f}%")

# After training your classifier (e.g., clf)
with open('classifiersematch.pkl', 'wb') as file:
    pickle.dump(clf, file)
