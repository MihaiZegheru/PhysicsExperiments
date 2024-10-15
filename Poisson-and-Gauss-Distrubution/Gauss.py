import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.stats import norm
import pandas as pd

data = np.array([
        [1, 1, 1, 5, 12, 13, 15, 30, 43, 42, 45, 43, 41, 37, 31, 22, 11, 13, 9, 4, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0.002, 0.007, 0.021, 0.050, 0.102, 0.179, 0.279, 0.397, 0.521, 0.639, 0.743, 0.825, 0.888, 0.932, 0.960, 0.978, 0.988, 0.994, 0.997, 0.999, 0.999, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
columns = ('Kexp(n)', 'nKexp(n)', 'P(n)', 'KthP(n)', 'PG(n)', 'KthG(n)')
rows = np.array([x for x in range(0, 24)])

for i in range(0, 24):
    data[1][i] = i * data[0][i]

N = 0
for i in range(0, 24):
    N += data[0][i]

E = 0
for i in range(0, 24):
    E += data[1][i]

for i in range(23, 0, -1):
    data[2][i] -= data[2][i - 1] 

for i in range(0, 24):
    data[3][i] = "{:.4f}".format(data[2][i] * N)

a = E / N
print(a)
s = math.sqrt(a)

for i in range(0, 24):
    data[4][i] = norm.cdf(i, loc=a, scale=s)

for i in range(23, 0, -1):
    data[4][i] -= data[4][i - 1]

for i in range(0, 24):
    data[5][i] = "{:.4f}".format(data[4][i] * N)

plt.bar(rows - 0.2 , data[0], 0.2, alpha=0.5)
plt.bar(rows, data[3], 0.2, alpha=0.5)
plt.bar(rows + 0.2, data[5], 0.2, alpha=0.5)
plt.legend(["Experimental", "Poisson", "Gauss"], loc="upper right")

pd_data = {"Kexp(n)": data[0],
           "nKexp(n)": data[1],
           "P(n)": data[2],
           "KthP(n)": data[3],
           "PG(n)": data[4],
           "KthG(n)": data[5]}
df = pd.DataFrame(pd_data)
df.to_csv('Normal.csv')

plt.show()
