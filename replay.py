import fastf1, fastf1.plotting
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fastf1.Cache.enable_cache('cache')
session = fastf1.get_session(2025, "Monza", "R")
session.load(telemetry=True, laps=True, weather=False, messages=False)
try:
    laps = session.laps
except Exception:
    raise SystemExit("Timing data didn't load. See the warnings above. Try another race or update fastf1.")
laps = session.laps

t0 = laps["LapStartTime"].min().total_seconds()
t1 = laps["Time"].max().total_seconds()
t = np.arange(t0, t1, 3.0)

xy={}
for num in session.drivers:
    abbr = session.get_driver(num)["Abbreviation"]
    p = session.pos_data[num]
    st = p["Time"].dt.total_seconds().values
    xy[abbr] = (np.interp(t, st, p["X"].values), np.interp(t, st, p["Y"].values))

tracks = laps.pick_fastest().get_telemetry()
fig, ax = plt.subplots(figsize=(8,8))
ax.plot(tracks["X"], tracks["Y"], color="gray", lw=10, alpha=0.3)
ax.set_aspect("equal");ax.axis("off")

dots = {a: ax.plot([], [], "o", ms=10,color = fastf1.plotting.get_driver_color(a, session))[0] for a in xy}
labels = {a: ax.text(0,0, a, fontsize=7) for a in xy}

def update(i):
    for a, (x,y) in xy.items():
        dots[a].set_data(x[i], y[i])
        labels[a].set_position((x[i] + 150, y[i]+150))
    ax.set_title(f"Race time: {t[i] - t0:.0f} s")
    return list(dots.values())

anim = FuncAnimation(fig, update, frames=len(t), interval= 40)
plt.show()