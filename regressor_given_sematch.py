import numpy as np
import pandas as pd
import ast
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def unpack_single_float_list(value):
    return ast.literal_eval(value)[0] if ast.literal_eval(value)[0] < 20 else 20

# Assuming your data is in a CSV file and the columns are named "Example 1", "Example 3", ..., "Last Example" for features and "Target" for the target
data = pd.read_excel("dataset_comparacion.xlsx")

data = data[(data['Score_num'] != -1) & (data['Score_num'] != "VACIO")]

feature_columns = ["Relacion_spacy_jcn", "Relacion_spacy_lch", "Relacion_spacy_li", "Relacion_spacy_lin", "Relacion_spacy_path", "Relacion_spacy_res", "Relacion_spacy_wpath", "Relacion_spacy_wup"]
X = data[feature_columns]
y = data["Score_num"]  # Target column

# Convert list of single float to single float
X = X.applymap(unpack_single_float_list)
#y = y.apply(lambda x: 1 if x > 0 else 0)

# Set up k-fold cross-validation with k=5
k = 5
kf = KFold(n_splits=k, random_state=42, shuffle=True)

# Initialize metrics
mse_scores = []
mae_scores = []
r2_scores = []

# Loop through the k-folds
for train_index, test_index in kf.split(X):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    # Create and train the Random Forest regressor
    regr = RandomForestRegressor(n_estimators=100, random_state=42)
    regr.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = regr.predict(X_test)

    # Calculate and store the mean squared error, mean absolute error, and R2 score
    mse_scores.append(mean_squared_error(y_test, y_pred))
    mae_scores.append(mean_absolute_error(y_test, y_pred))
    r2_scores.append(r2_score(y_test, y_pred))

# Calculate and display the average mean squared error, mean absolute error, and R2 score
avg_mse = np.mean(mse_scores)
avg_mae = np.mean(mae_scores)
avg_r2 = np.mean(r2_scores)
print(f"Average Mean Squared Error: {avg_mse:.2f}")
print(f"Average Mean Absolute Error: {avg_mae:.2f}")
print(f"Average R2 Score: {avg_r2:.2f}")
