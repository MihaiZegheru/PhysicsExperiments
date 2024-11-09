import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats, interpolate
import numpy as np

IN_PATH = "Light-Diffraction/in/"
OUT_PATH = "Light-Diffraction/out/"
DATA_FILES = ["data3.csv", "data4.csv", "data5.csv"]
TABLE3 = "table3"
TABLE3_FILES = ["table3A.csv", "table3B.csv", "table3C.csv"]
a = {
	'A': 0.12,
	'B': 0.24,
	'C': 0.48,
}
D = 1810
eps = {
	'A': 4.493,
	'B': 7.725,
	'C': 10.904,
}
I = {
	'A': 0.0472,
	'B': 0.0168,
	'C': 0.00834,
}
# g/mm^2
RCu = 89000
RFe = 78000
RAl = 27000

legend_materials = []

def solve(file):
	df = pd.read_csv(IN_PATH + file)
	size = df['U(mV)'].size
	x = np.arange(-size / 2, size / 2)
	f = interpolate.interp1d(x, df['U(mV)'], kind='cubic')
	xnew = np.linspace(x[0], x[-1], 1000)
	ynew = f(xnew)
	plt.xticks(x)
	plt.plot(xnew, ynew)
	plt.show()

extlmb = []
extlmb = np.array(extlmb)

def solve3(file, msr):
	global extlmb
	df = pd.read_csv(IN_PATH + file)
	xmax = np.array(df['xmax(mm)'])
	xmin = np.array(df['xmin(mm)'])
	xmin = xmin[:-1]
	Xmn = []
	for i in range(0, int(xmin.size / 2)):
		Xmn.append(abs(xmin[i] - xmin[xmin.size - i - 1]) / 2)
	Xmn = np.array(Xmn)
	print(type(Xmn))
	lmb = (Xmn * a[msr] / D) * [1/3, 1/2, 1] * 1e6
	extlmb = np.stack((extlmb, lmb), axis=1)
	# print(lmb.mean)
	print(xmax, xmin, Xmn, lmb)

# for file in DATA_FILES:
	# solve(file)

for l in ['A', 'B', 'C']:
	solve3(TABLE3 + l + '.csv', l)
# for file in TABLE3_FILES:
	# solve3(file, )
print(extlmb.mean)
