import pandas as pd

def build_features(df):
    df = df.sort_values(["year", "round"]).reset_index(drop=True)
    finished = df["status"].fillna("").str.contains(r"Finished|\+\d+ Lap")
    df["dnf"] = (~finished).astype(float).where(df["status"].notna())

    def driver_roll(col, n=5):
        return df.groupby("driver")[col].transform(lambda s: s.shift(1).rolling(n, min_periods=1).mean())
    df["driver_finish_form"] = driver_roll("finish")
    df["driver_quali_form"] = driver_roll("quali_pos")
    df["driver_dnf_rate"] = driver_roll("dnf",10)
    
    for col in ["finish", "quali_pos"]:
        t = (df.groupby(["team", "year", "round"], as_index=False)[col].mean().sort_values(["year", "round"]))
        name = f"team_{col}_form"
        t[name] = t.groupby("team")[col].transform(lambda s: s.shift(1).rolling(6, min_periods=1).mean())
        df = df.merge(t[["team", "year", "round", name]], on=["team", "year", "round"], how="left")

    for col, name in [("finish", "track_finish_history"), ("quali_pos", "track_quali_history")]:
        df[name] = df.groupby(["driver", "event"])[col].transform(lambda s: s.shift(1).expanding().mean())
        return df


quali_feats = ["driver_quali_form", "team_quali_pos_form", "track_quali_history"]
race_feats = ["driver_finish_form", "team_finish_form", "driver_dnf_rate", "track_finish_history", "grid"]

from features import build_features
df = build_features(pd.read_csv("results.csv"))
print(df[df.driver=="VER"][["year","round","finish","driver_finish_form"]].tail(8))