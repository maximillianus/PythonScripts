"""
Feature Scalingl method and techniques
"""

import random
from statistics import mean
from statistics import stdev

# dataset
random.seed(1)
x = random.sample(range(20), 5)
print('Original Data:', x)

# Rescaling method
# Giving range of  0 to 1
def rescaling(x):
    x_numer = [i - min(x) for i in x]
    x_denom = max(x) - min(x)
    x_ = [i / x_denom for i in x_numer]
    return x_

# Mean Normalization method
# Giving range of -1 to 1
def mean_normalization(x):
    x_numer = [i - mean(x) for i in x]
    x_denom = max(x) - min(x)
    x_ = [i / x_denom for i in x_numer]
    return x_

# Standardization method
def standardization(x):
    x_numer = [i - mean(x) for i in x]
    x_denom = stdev(x)
    x_ = [i / x_denom for i in x_numer]
    x_ = [round(i, 2) for i in x_]
    return x_

rescaled_x = rescaling(x)
normalized_x = mean_normalization(x)
standardized_x = standardization(x)

print('Rescaling method result:', rescaled_x)
print('Mean Normalization method result:', normalized_x)
print('Standardization method result:', standardized_x)
