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

#data = data[(data['Score_num'] != -1) & (data['Score_num'] != "VACIO")]

feature_columns = ["Relacion_spacy_jcn", "Relacion_spacy_lch", "Relacion_spacy_li", "Relacion_spacy_lin", "Relacion_spacy_path", "Relacion_spacy_res", "Relacion_spacy_wpath", "Relacion_spacy_wup"]
X = data[feature_columns]  # Feature columns
y = data["Score_num"]  # Target column

# Convert list of single float to single float
X = X.applymap(unpack_single_float_list)
#y = y.apply(lambda x: 1 if x > 0 else 0)

# Load the classifier from the pickle file
with open('classifiersematchrandomforest.pkl', 'rb') as file:
    classifier = pickle.load(file)

# Use the loaded classifier to make predictions
predictions = classifier.predict(X)

# Use the loaded classifier to predict probabilities
probabilities = classifier.predict_proba(X)

# Add probabilities to the dataframe
X['Probability_Class_0'] = probabilities[:, 0]  # Probability of class 0
X['Probability_Class_1'] = probabilities[:, 1]  # Probability of class 1


# Add predictions to the dataframe
X['Predictions'] = predictions

# Output the result to an Excel file
X.to_excel('results_tot_classifier_sematch.xlsx', index=False)