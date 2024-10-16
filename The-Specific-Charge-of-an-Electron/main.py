from math import sqrt, pi
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

IN_PATH = "The-Specific-Charge-of-an-Electron/in/"
OUT_PATH = "The-Specific-Charge-of-an-Electron/out/"

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
	a = (125 / 32) * (R**2 / (u0**2 * n**2)) * (1/slope)
	print(a)
	plt.show()

def taskOne():
	df = pd.read_csv(IN_PATH + "data1.csv")
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
	df.to_csv(OUT_PATH + "data1.csv");
					  
def solveForR(df):
	print(df)
	x = []
	y = []
	idx = 0
	for idx, row in df.iterrows():
		df.loc[idx, 'e/m'] = computeCharge(df.loc[idx, 'r'], df.loc[idx, 'U'],
																		 computeMagneticField(df.loc[idx, 'I']))
		df.loc[idx, 'Im'] = df['I'].mean()
		x.append(df.loc[idx, 'U'] / (df.loc[idx, 'r']**2))
		y.append(df.loc[idx, 'I']**2)

	for idx, row in df.iterrows():
		df.loc[idx, 'SIm'] = computeStandardDeviationOfCurrent(df['I'], df.loc[idx, 'Im'])
		df.loc[idx, 'EIm'] = df.loc[idx, 'SIm'] / df.loc[idx, 'Im']
	df.to_csv(OUT_PATH + f"data2-r={df.loc[idx, 'r']}.csv")
	plotLinearRegression(x, y, 'U/r^2 (V/m)', 'I^2 (A^2)')

def taskTwo():
	df = pd.read_csv(IN_PATH + "data2.csv")
	df.groupby(['r']).apply(solveForR)

def plotForU(df):
	x = []
	y = []
	for idx, row in df.iterrows():
		x.append(df.loc[idx, 'U'] / (df.loc[idx, 'r']**2))
		y.append(df.loc[idx, 'I']**2)
	plotLinearRegression(x, y, 'U/r^2 (V/m)', 'I^2 (A^2)')

def solveForU(df, Ims, ps):
	for idx, row in df.iterrows():
		df.loc[idx, 'e/m'] = computeCharge(df.loc[idx, 'r'], df.loc[idx, 'U'],
																		 computeMagneticField(df.loc[idx, 'I']))
		# df.loc[idx, 'Im'] = df.groupby(['U'] == df.loc[idx, 'U'])['I'].mean()
		print(df.loc[idx, 'e/m'] * 1E-11)
		df.loc[idx, '1/r'] = 1 / df.loc[idx, 'r']
	df.to_csv(OUT_PATH + "data3.csv")

def solveCompositesForU(df):
	Ims = []
	ps = []
	for gr in df.groupby(['U']):
		Ims.append(gr[1]['I'].mean())

		x = []
		y = []
		for idx, row in gr[1].iterrows():
			x.append(df.loc[idx, 'U'] / (df.loc[idx, 'r']**2))
			y.append(df.loc[idx, 'I']**2)
		slope, intercept, r, p, std_err = stats.linregress(x, y)
		ps.append(slope)
	return (Ims, ps)

	
def taskThree():
	df = pd.read_csv(IN_PATH + "data3.csv")
	# (Ims, ps) = solveCompositesForU(df);
	# solveForU(df, Ims, ps)
	df.groupby(['U']).apply(solveForU)

# taskOne()
taskTwo()
# taskThree()
# print(df)


