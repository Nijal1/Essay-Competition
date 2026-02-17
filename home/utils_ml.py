from joblib import load

dt_model = load("home/ml/decision_tree.joblib")
lr_model = load("home/ml/linear_regression.joblib")

def predict_score(grammar, spelling, total, words, model="dt"):
    X = [[grammar, spelling, total, words]]

    if model == "lr":
        return round(lr_model.predict(X)[0], 2)

    return round(dt_model.predict(X)[0], 2)
