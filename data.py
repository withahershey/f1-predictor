import fastf1
import pandas as pd

fastf1.Cache.enable_cache('cache') 

def weekend(year, round):
    q = fastf1.get_session(year, round, "Q")
    r = fastf1.get_session(year, round, "R")
    for s in (q, r):
        s.load(laps=False, telemetry=False, weather=False, messages=False)

    qr = q.results[["Abbreviation", "TeamName", "Position"]].rename(
            columns={"Abbreviation": "driver", "TeamName": "team", "Position": "quali_pos"})
       
    rr = r.results[["Abbreviation", "GridPosition", "Position", "Status"]].rename(
            columns={"Abbreviation": "driver", "GridPosition": "grid","Position": "finish", "Status": "status"})

    out = qr.merge(rr, on="driver", how="outer")
    out["grid"] = out["grid"].replace(0, 20)
    out["year"] = year
    out["round"] = round
    out["event"] = r.event["EventName"]
    return out

if __name__ == "__main__":
    rows = []
    for year in range(2018, pd.Timestamp.now().year + 1):
        sched = fastf1.get_event_schedule(year, include_testing=False)
        for _, ev in sched.iterrows():
            if ev["EventDate"] > pd.Timestamp.now():
                continue
            try:
                rows.append(weekend(year, ev["RoundNumber"]))
                print("loaded", year, ev["EventName"])
            except Exception as e:
                print("skipped", year, ev["EventName"], "->", e)
    pd.concat(rows).to_csv("results.csv", index=False)