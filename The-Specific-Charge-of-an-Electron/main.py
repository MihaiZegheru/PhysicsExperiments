from math import sqrt, pi
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

DATA1_FILE = "The-Specific-Charge-of-an-Electron/in/data1.csv"
DATA2_FILE = "The-Specific-Charge-of-an-Electron/in/data2.csv"

N = 5
u0 = 4 * pi * 1E-7
n = 154
R = 0.2

def computeAverageCurrentValue(currents):
	return sum(currents) / len(currents)

def computeStandardDeviationOfCurrent(currents, Im):
	sum = 0
	for curr in currents:
		sum += (curr - Im)**2
	return sqrt(sum / (N * (N - 1)))

def computeMagneticField(Im):
	return ((4 / 5) ** (3 / 2)) * u0 * n * Im / R

def computeCharge(r, U, B):
	return (2 * U) / (B**2 * r**2)

def computeExperimentalCharges(currents, r, U):
	charges = []
	for curr in currents:
		charges.append(computeCharge(r, U, computeMagneticField(curr)))
	return charges

def plotLinearRegression(x, y, xlabel, ylabel):
	slope, intercept, r, p, std_err = stats.linregress(x, y)
	foo = lambda x : x * slope + intercept
	plt.scatter(x, y)
	plt.plot(x, list(map(foo, x)))
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.figtext(0.5, 0.01, f"y = x * {slope} + {intercept}", ha="center",
						 fontsize=13)
	plt.show()

def taskOne():
	df = pd.read_csv(DATA1_FILE)
	for idx, row in df.iterrows():
		currents = [row['I1'], row['I2'], row['I3'], row['I4'], row['I5']]
		df.loc[idx, 'Im'] = computeAverageCurrentValue(currents)
		df.loc[idx, 'SIm'] = computeStandardDeviationOfCurrent(currents,
																												 df.loc[idx, 'Im'])
		df.loc[idx, 'EIm'] = df.loc[idx, 'SIm'] / df.loc[idx, 'Im']
		df.loc[idx, 'B'] = computeMagneticField(df.loc[idx, 'Im'])
		df.loc[idx, 'e/m'] = computeCharge(df.loc[idx, 'r'], df.loc[idx, 'U'],
																		 df.loc[idx, 'B'])
		charges = computeExperimentalCharges(currents, df.loc[idx, 'r'],
																			 df.loc[idx, 'U'])
		plotLinearRegression(currents, charges, 'I(A)', 'e/m (C/kg)')

def solveForR(df):
	x = []
	y = []
	for idx, row in df.iterrows():
		df.loc[idx, 'e/m'] = computeCharge(df.loc[idx, 'r'], df.loc[idx, 'U'],
																		 computeMagneticField(df.loc[idx, 'I']))
		x.append(df.loc[idx, 'U'] / (df.loc[idx, 'r']**2))
		y.append(df.loc[idx, 'I']**2)
	plotLinearRegression(x, y, 'U/r^2 (V/m)', 'I^2 (A^2)')

def taskTwo():
	df = pd.read_csv(DATA2_FILE)
	df.groupby(['r']).apply(solveForR)

# taskOne()
taskTwo()
# print(df)


