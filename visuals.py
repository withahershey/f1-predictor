import numpy as np
import matplotlib.pyplot as plt
import fastf1
from predict import next, EVENT


res_std = 6.352587324966774
N = 10_000

noise = np.random.normal(0, res_std, (len(next), N))
sims = next["pred_finish"].values[:, None] + noise
ranks = sims.argsort(axis=0).argsort(axis=0) + 1

next["podium_prob"] = (ranks <= 3).mean(axis=1)
top= next.sort_values("podium_prob", ascending=False).head(10)
plt.barh(top.driver [::-1], top.podium_prob[::-1] *100)
plt.xlabel("Podium Probability (%)"); plt.title(f"Podium Probabilities for {EVENT}"); plt.xlim(0,100); plt.grid(axis="x")
plt.show()

session = fastf1.get_session(2025, "Monza", "R")
session.load(telemetry=True, laps=True, weather=False, messages=False)
print(session.laps.columns.tolist())
print(session.pos_data["1"].head())