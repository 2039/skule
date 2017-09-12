import numpy as np
import math as m
import matplotlib.pyplot as plt

# P(Z = 1) = sum(1,n) of P(Z = 1|Y = i)P(Y = i) = k/n * (sum(k+1,n) of (1/(i-1))) ~ (k/n) * ln(n/k)

# Fix n = 30 and simulate P(Z = 1)
N1 = 30
K1 = [k for k in range(1, N1)]
Y1 = [k / N1 * m.log(N1 / k) for k in K1]
plt.plot(K1, Y1, color="blue", label="P(Z = 1| N = 30)")

# Fix n = 40 and simulate P(Z = 1)
N2 = 40
K2 = [k for k in range(1, N2)]
Y2 = [k / N2 * m.log(N2 / k) for k in K2]
plt.plot(K2, Y2, color="red", label="P(Z = 1| N = 40)")

# Interpretation: The probability of selecting the best secretary, when n is fixed to 30, rises as one approaches
# k ~ 11 and decreases as one approaches k = 30. The tendency is analogous when n is fixed to 40, but this time the
# maximum probability is reached when k ~ 15.

#Bruk print-f-funksjon for å skrive ut max y-verdi i begge tilfeller.

plt.show()
