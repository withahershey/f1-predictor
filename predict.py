import pandas as pd
from data import real_grid
from features import build_features, quali_feats, race_feats
from model import fit

hist = pd.read_csv("results.csv")
quali_model = fit(build_features(hist), quali_feats, "quali_pos")
race_model = fit(build_features(hist), race_feats, "finish")

year = int(hist.year.max())
next_round = int(hist[hist.year==year][ "round"].max()) + 1
event = "Name Of Next  Grand Prix"

last = hist[(hist.year==year) & (hist["round"] == next_round - 1)]
future = last[["driver", "team"]].assign(year=year, round=next_round, event=event)

full = build_features(pd.concat([hist, future], ignore_index=True))
next = full[(full.year == year) &(full["round"] == next_round)].copy()

next["quali_pred"] = quali_model.predict(next[quali_feats])
next["quali_rank"] = next["quali_pred"].rank(method="first")

next["grid"] = next["quali_rank"]
next["predicted_finish"] = race_model.predict(next[race_feats])
real_quali = False

if real_quali:
    real = real_grid(year, next_round)
    next = next.drop(columns="grid").merge(real, on="driver", how="left")
    next["pred_finish"] = race_model.predict(next[race_feats])
    next["race_rank"] = next["pred_finish"].rank(method="first")
next["race_rank"] = next["predicted_finish"].rank(method="first")

if __name__ == "__main__":
    print(next.sort_values("race_rank")[["driver","team","quali_rank","race_rank"]])