import matplotlib.pyplot as plt
import numpy as np

# Simple Scatter Plot
x = list(range(-5,6))
y = [el*2 for el in x]
# plt.scatter(x=x,y=y)
# plt.show()

# Simple line plot
y = [el**2 for el in x]
# plt.plot(x,y)
# plt.show()

# sigmoid function
# y = 1 / (1 + exp(-x))
y1 = [1/(1 + np.exp(-el)) for el in x]
y2 = [np.exp(el)/(np.exp(el) + 1) for el in x]
y = y2
print(x)
print(y)
# plt.plot(x,y)
# plt.show()

# sigmoid derivative
y1 = [el*(1-el) for el in x]
y = y1
print(x)
print(y)
plt.plot(x,y)
plt.show()