import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

a = 'c:/Users/USER/OneDrive/DESKTOP/wait.txt'

d = []
e = []

with open(a, 'r') as file:
    for line in file:
        parts = line.split()
        d.append(parts[0])
        e.append(int(parts[1]))

fig, ax = plt.subplots()
bars = ax.bar(d, e)

ax.set_title("visualisation")
ax.set_xlabel("items")
ax.set_ylabel("values")

# animation function
def update(frame):
    for i, bar in enumerate(bars):
        base = e[i]
        # create up and down motion
        new_height = base + np.sin(frame/5) * (base * 0.3)
        bar.set_height(new_height)

ani = FuncAnimation(fig, update, interval=100)

plt.show()