import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from joblib import dump

# Sample dataset (replace later with real data)
data = {
    "grammar_errors": [2, 5, 1, 8, 0],
    "spelling_errors": [1, 3, 0, 4, 0],
    "total_errors": [3, 8, 1, 12, 0],
    "word_count": [250, 200, 300, 150, 400],
    "score": [90, 70, 95, 60, 100],
}

df = pd.DataFrame(data)

X = df.drop("score", axis=1)
y = df["score"]

# Models
dt = DecisionTreeRegressor()
lr = LinearRegression()

dt.fit(X, y)
lr.fit(X, y)

dump(dt, "home/ml/decision_tree.joblib")
dump(lr, "home/ml/linear_regression.joblib")

print("Models trained and saved")
