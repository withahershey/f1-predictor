import pandas as pd
import numpy as np
from scipy.stats import spearmanr
from sklearn.ensemble import HistGradientBoostingRegressor
from features import build_features, quali_feats,race_feats

def fit(train, feats, target):
    d = train.dropna(subset=[target])
    m = HistGradientBoostingRegressor(max_depth = 5, learning_rate = 0.05, max_iter = 1000, random_state = 42)
    return m.fit(d[feats], d[target])

def per_race_spearman(d, pred, target):
    scores = [spearmanr(g[pred], g[target]).correlation for _, g in d.groupby(["year", "round"])]
    return np.nanmean(scores)

if __name__ == "__main__":
    df = build_features(pd.read_csv("results.csv"))
    last_year = df["year"].max()
    train = df[df["year"] < last_year]
    test = df[df["year"] == last_year].dropna(subset=["quali_pos", "finish"]).copy()
    
    quali_model = fit(train, quali_feats, "quali_pos")
    race_model = fit(train, race_feats, "finish")
    test["quali_pred"] = quali_model.predict(test[quali_feats])
    test["race_pred"] = race_model.predict(test[race_feats])

    print("Quali Spearman:", per_race_spearman(test, "quali_pred", "quali_pos"))
    print("Race Spearman :", per_race_spearman(test, "race_pred", "finish"))
    print("baseline finish=grid", per_race_spearman(test, "grid", "finish"))
    print("race mea(# of pos off):",(test.race_pred - test.finish).abs().mean())
    print("residual stddev:", (test.race_pred - test.finish).std())

    test["err"] = (test.race_pred - test.finish).abs()
    print(test.groupby("event").err.mean().sort_values(ascending=False).head(5))
    print(test.groupby("driver").err.mean().sort_values(ascending=False).head(5))