import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.stats import norm
import pandas as pd

data = np.array([
        [11, 45, 72, 80, 88, 55, 35, 25, 4, 3, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0.0273, 0.1257, 0.3027, 0.5152, 0.7064, 0.8441, 0.9267, 0.9692, 0.9883, 0.9960, 0.9987],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
columns = ('Kexp(n)', 'nKexp(n)', 'P(n)', 'KthP(n)', 'PG(n)', 'KthG(n)')
rows = np.array([x for x in range(0, 11)])

for i in range(0, 11):
    data[1][i] = i * data[0][i]

N = 0
for i in range(0, 11):
    N += data[0][i]

E = 0
for i in range(0, 11):
    E += data[1][i]

for i in range(10, 0, -1):
    data[2][i] -= data[2][i - 1] 

for i in range(0, 11):
    data[3][i] = "{:.4f}".format(data[2][i] * N)


a = E / N
print(a)
s = math.sqrt(a)

for i in range(0, 11):
    data[4][i] = norm.cdf(i, loc=a, scale=s)

for i in range(10, 0, -1):
    data[4][i] -= data[4][i - 1]

for i in range(0, 11):
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
df.to_csv('Poisson.csv')

plt.show()
