import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

IN_PATH = "Debye-Scherrer-Electron-Diffraction/in/"
OUT_PATH = "Debye-Scherrer-Electron-Diffraction/out/"

d1 = 2.13 * 1e-10 # m
d2 = 1.23 * 1e-10 # m
L = 13.5 # cm

e = 1.602 * 1e-19 # C
m = 9.109 * 1e-31 # kg
h = 6.625 * 1e-34 # Js

def plotLinearRegression(x, y, xlabel, ylabel):
	slope, intercept, r, p, std_err = stats.linregress(x, y)
	foo = lambda x : x * slope + intercept
	plt.scatter(x, y)
	plt.plot(x, list(map(foo, x)))
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)

def plotForDAndOneOverSqrtU(df):
	plotLinearRegression(df['1/sqrt(U)(V^(-1/2))'], df['D1(cm)'], '1/sqrt(U)(V^(-1/2))', 'D1(cm)')
	plt.show()
	plotLinearRegression(df['1/sqrt(U)(V^(-1/2))'], df['D2(cm)'], '1/sqrt(U)(V^(-1/2))', 'D2(cm)')
	plt.show()
	# legend_materials.append(f"{df.name}_value")
	# legend_materials.append(f"{df.name}_attenuation_slope")

def determine_d(oneOverSqrtU, D):
	slope, intercept, r, p, std_err = stats.linregress(oneOverSqrtU, D * 1e-2)
	d = (2 * h * L * 1e-2) / (slope * np.sqrt(2 * m * e))
	return d

def taskOne():
	df = pd.read_csv(IN_PATH + "data.csv")

	df['1/sqrt(U)(V^(-1/2))'] = 1 / np.sqrt(df['U(kV)'] * 1e3)
	df['lmbE1(pm)'] = (d1 * df['D1(cm)'] / (2 * L)) * 1e10
	df['lmbE2(pm)'] = (d2 * df['D2(cm)'] / (2 * L)) * 1e10
	df['lmbT(pm)'] = (h / np.sqrt(2 * m * e * df['U(kV)'] * 1e3)) * 1e10
	plotForDAndOneOverSqrtU(df)
	print("d1: " + str(determine_d(df['1/sqrt(U)(V^(-1/2))'], df['D1(cm)'])) + " (m)")
	print("d2: " + str(determine_d(df['1/sqrt(U)(V^(-1/2))'], df['D2(cm)'])) + " (m)")
	df.to_csv(OUT_PATH + "data.csv")

taskOne();
