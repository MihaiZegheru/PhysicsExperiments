import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

IN_PATH = "Solid-Angle/in/"
OUT_PATH = "Solid-Angle/out/"

lmb = 219.7
S = 0.85
D = 4.5
T = 1e-6
f = 1.35  # TODO N pt inf per s
sf = np.sqrt(190) / 140


legend_materials = []

#  Toate 3 graficele pe unul
def plotLinearRegression(x, y, xlabel, ylabel):
	slope, intercept, r, p, std_err = stats.linregress(x, y)
	foo = lambda x : x * slope + intercept
	plt.scatter(x, y)
	plt.plot(x, list(map(foo, x)))
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.show()

def taskOne():
	df = pd.read_csv(IN_PATH + "data.csv")

	df["O/4pi"] = 1 / 2 - 1 / np.sqrt(4 + pow((D / df["r(cm)"]), 2))

	slope, intercept, r, p, std_err = stats.linregress(df["O/4pi"], df["N(imp)"])
	eps = slope / (lmb * S)
	print(f"Eps is {eps}")

	df["sN"] = np.sqrt(df["N(imp)"])
	df["n\'"] = df["N(imp)"] / df["t(s)"]
	df["sn\'"] = np.sqrt(df["N(imp)"]) / df["t(s)"]
	df["n\'\'"] = df["n\'"] / (1 - T * df["n\'"])
	df["sn\'\'"] = df["sn\'"] / pow((1 - T * df["n\'"]), 2)
	df["n"] = df["n\'\'"] - f
	df["sn"] = np.sqrt(pow(df["sn\'\'"], 2) + sf**2)

	df.to_csv(OUT_PATH + "data.csv")
	plotLinearRegression(df["O/4pi"], df["N(imp)"], "O/4pi", "N(imp)")


taskOne();
