import numpy as np
import pandas as pd
import ast
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_recall_fscore_support
from sklearn import svm
import pickle

def unpack_single_float_list(value):
    return (ast.literal_eval(value)[0] if ast.literal_eval(value)[0] < 20 else 20) if not isinstance(value, bool) else value

data = pd.read_excel("dataset_comparacion.xlsx")

data = data[(data['Score_num'] != -1) & (data['Score_num'] != "VACIO")]

feature_columns = [
    "Relacion_spacy_jcn", 
    "Relacion_spacy_lch", 
    "Relacion_spacy_li", 
    "Relacion_spacy_lin", 
    "Relacion_spacy_path", 
    "Relacion_spacy_res", 
    "Relacion_spacy_wpath", 
    "Relacion_spacy_wup", 
    "Eval_spacy_senses", 
    "Eval_spacybabel_categories"
]
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
    ''''
    Average Accuracy: 60.37%
    Average Precision: 61.69%
    Average Recall: 60.37%
    Average F-score: 52.33%
    '''
    clf = svm.SVC(kernel='linear')

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
with open('classifierbabel.pkl', 'wb') as file:
    pickle.dump(clf, file)
