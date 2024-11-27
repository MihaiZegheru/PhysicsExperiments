import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats, interpolate
import numpy as np

IN_PATH = "Fotoelectric-Effect-Plank/in/"
OUT_PATH = "Fotoelectric-Effect-Plank/out/"
DATA_FILES = ["yellow.csv", "green.csv", "blue.csv", "violet.csv"]

legend_materials = []

c = 3 * 1e8 # m/s

def plotLinearRegression(x, y, xlabel, ylabel, title):
	slope, intercept, r, p, std_err = stats.linregress(x, y)
	foo = lambda x : x * slope + intercept
	plt.figure(figsize=(8,7))
	plt.title(title)
	plt.get_current_fig_manager().set_window_title(title)
	plt.scatter(x, y)
	plt.plot(x, list(map(foo, x)))
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.figtext(0.5, 0.01, f"y = x * {slope} + {intercept}", ha="center",
						 fontsize=13)
	plt.show()

def solve(file):
	df = pd.read_csv(IN_PATH + file)
	df["frv(1e12 Hz)"][0] = (c / (df["lmb(nm)"][0] / 1e9)) / 1e12
	U0_arr = []
	for i in range(1, 11):
		U0_arr.append(df[f"U0{i}(V)"][0])
	df["U0med(V)"][0] = sum(U0_arr) / 10
	df.to_csv(OUT_PATH + file)
	return (df["U0med(V)"][0], df["frv(1e12 Hz)"][0])


Umed = []
frv = []
for file in DATA_FILES:
	(u, f) = solve(file)
	Umed.append(u)
	frv.append(f)

print(frv)
print(Umed)

plotLinearRegression(x=frv, y=Umed,
					 ylabel=['UmedY', 'UmedG', 'UmedB', 'UmedV', 'UmedU'],
					 xlabel=['frvY', 'frvG', 'frvB', 'frvV', 'frvU'],
					 title="U med dependency on frequency")


