import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

IN_PATH = "Attenuation-Coefficient-for-Gamma-Radiation/in/"
OUT_PATH = "Attenuation-Coefficient-for-Gamma-Radiation/out/"

# g/mm^2
RCu = 89000
RFe = 78000
RAl = 27000

legend_materials = []

#  Toate 3 graficele pe unul
def plotLinearRegression(x, y, xlabel, ylabel):
	slope, intercept, r, p, std_err = stats.linregress(x, y)
	print(slope)
	foo = lambda x : x * slope + intercept
	plt.scatter(x, y)
	plt.plot(x, list(map(foo, x)))
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)

def plotForMaterialAndA1(df):
	if (df.name == 'Air'):
		return
	plotLinearRegression(df['thickness(mm)'], df['A1'], 'Thickness (mm)', 'ln(A1)')
	legend_materials.append(f"{df.name}_value")
	legend_materials.append(f"{df.name}_attenuation_slope")

def plotForMaterialAndA2(df):
	if (df.name == 'Air'):
		return
	plotLinearRegression(df['thickness(mm)'], df['A2'], 'Thickness (mm)', 'ln(A2)')
	legend_materials.append(f"{df.name}_value")
	legend_materials.append(f"{df.name}_attenuation_slope")

def solveForMaterial(df):
	slope, intercept, r, p, std_err = stats.linregress(df['thickness(mm)'], df['A1'])
	df['u1(1/mm)'] = slope
	slope, intercept, r, p, std_err = stats.linregress(df['thickness(mm)'], df['A2'])
	df['u2(1/mm)'] = slope

	if df.name == 'Cu':
		df['u1/R(mm/g)'] = df['u1(1/mm)'] / RCu
		df['u2/R(mm/g)'] = df['u2(1/mm)'] / RCu
	elif df.name == 'Fe':
		df['u1/R(mm/g)'] = df['u1(1/mm)'] / RFe
		df['u2/R(mm/g)'] = df['u2(1/mm)'] / RFe
	elif df.name == 'Al':
		df['u1/R(mm/g)'] = df['u1(1/mm)'] / RAl
		df['u2/R(mm/g)'] = df['u2(1/mm)'] / RAl
	df.to_csv(OUT_PATH + f"data-{df.name}.csv")

def taskOne():
	df = pd.read_csv(IN_PATH + "data.csv")

	f1 = df.loc[df['material'] == 'Air','A1'][0]
	f2 = df.loc[df['material'] == 'Air', 'A2'][0]
	df['correctedA1'] = df['A1'] - f1
	df['correctedA2'] = df['A2'] - f2
	df['ln(A1)'] = np.log2(df['correctedA1'])
	df['ln(A2)'] = np.log2(df['correctedA2'])

	df.groupby(['material']).apply(solveForMaterial)

	legend_materials.clear()
	df.groupby(['material']).apply(plotForMaterialAndA1)
	plt.legend(legend_materials, loc="upper right")
	plt.show()

	legend_materials.clear()
	df.groupby(['material']).apply(plotForMaterialAndA2)
	plt.legend(legend_materials, loc="upper right")
	plt.show()

taskOne();
