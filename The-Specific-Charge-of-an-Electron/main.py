from math import sqrt, pi
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
from decimal import Decimal

IN_PATH = "The-Specific-Charge-of-an-Electron/in/"
OUT_PATH = "The-Specific-Charge-of-an-Electron/out/"

N = 5
u0 = 4 * pi * 1E-7
n = 154
R = 0.2

# From https://stackoverflow.com/questions/6913532/display-a-decimal-in-scientific-notation
def format_decimal(x, prec=3):
    tup = x.as_tuple()
    digits = list(tup.digits[:prec + 1])
    sign = '-' if tup.sign else ''
    dec = ''.join(str(i) for i in digits[1:])
    exp = x.adjusted()
    return '{sign}{int}.{dec}E{exp}'.format(sign=sign, int=digits[0], dec=dec, exp=exp)

def toSci(num):
	return format_decimal(Decimal(num))

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
	a = (125 / 32) * (R**2 / (u0**2 * n**2)) * (1/slope)
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
		plotLinearRegression(currents, charges, 'I(A)', 'e/m (C/kg)', "r=25mm - const, U=160V - const")
	for idx, row in df.iterrows():
		df.loc[idx, 'Im'] = toSci(df.loc[idx, 'Im'])
		df.loc[idx, 'SIm'] = toSci(df.loc[idx, 'SIm'])
		df.loc[idx, 'EIm'] = toSci(df.loc[idx, 'EIm'])
		df.loc[idx, 'B'] = toSci(df.loc[idx, 'B'])
		df.loc[idx, 'e/m'] = toSci(df.loc[idx, 'e/m'])
	df.to_csv(OUT_PATH + "data1.csv");
					  
def solveForR(gf, df):
	x = []
	y = []
	idx = 0
	for idx, row in gf.iterrows():
		df.loc[idx, 'e/m'] = computeCharge(df.loc[idx, 'r'], df.loc[idx, 'U'],
																		 computeMagneticField(df.loc[idx, 'I']))
		df.loc[idx, 'Im'] = gf['I'].mean()
		x.append(df.loc[idx, 'U'] / (df.loc[idx, 'r']**2))
		y.append(df.loc[idx, 'I']**2)
	for idx, row in gf.iterrows():
		df.loc[idx, 'SIm'] = computeStandardDeviationOfCurrent(gf['I'], df.loc[idx, 'Im'])
		df.loc[idx, 'EIm'] = df.loc[idx, 'SIm'] / df.loc[idx, 'Im']
	
	plotLinearRegression(x, y, 'U/r^2 (V/m)', 'I^2 (A^2)', f"r={df.loc[idx, 'r']} - const")
	for idx, row in gf.iterrows():
		df.loc[idx, 'Im'] = toSci(df.loc[idx, 'Im'])
		df.loc[idx, 'SIm'] = toSci(df.loc[idx, 'SIm'])
		df.loc[idx, 'EIm'] = toSci(df.loc[idx, 'EIm'])
		df.loc[idx, 'e/m'] = toSci(df.loc[idx, 'e/m'])

def taskTwo():
	df = pd.read_csv(IN_PATH + "data2.csv")
	df.groupby(['r']).apply(solveForR, df)
	df.to_csv(OUT_PATH + "data2.csv")

def solveForU(gf, df):
	x = []
	y = []
	idx = 0
	for idx, row in gf.iterrows():
		df.loc[idx, 'e/m'] = computeCharge(df.loc[idx, 'r'], df.loc[idx, 'U'],
																		 computeMagneticField(df.loc[idx, 'I']))
		df.loc[idx, 'Im'] = gf['I'].mean()
		x.append(1 / df.loc[idx, 'r'])
		y.append(df.loc[idx, 'I'])
	for idx, row in gf.iterrows():
		df.loc[idx, 'SIm'] = computeStandardDeviationOfCurrent(gf['I'], df.loc[idx, 'Im'])
		df.loc[idx, 'EIm'] = df.loc[idx, 'SIm'] / df.loc[idx, 'Im']
	
	plotLinearRegression(x, y, '1/r (m^-1)', 'I (A)', f"U={df.loc[idx, 'U']} - const")
	for idx, row in gf.iterrows():
		df.loc[idx, 'Im'] = toSci(df.loc[idx, 'Im'])
		df.loc[idx, 'SIm'] = toSci(df.loc[idx, 'SIm'])
		df.loc[idx, 'EIm'] = toSci(df.loc[idx, 'EIm'])
		df.loc[idx, 'e/m'] = toSci(df.loc[idx, 'e/m'])
	
def taskThree():
	df = pd.read_csv(IN_PATH + "data3.csv")
	df.groupby(['U']).apply(solveForU, df)
	df.to_csv(OUT_PATH + "data3.csv")

taskOne()
taskTwo()
taskThree()
# print(df)


