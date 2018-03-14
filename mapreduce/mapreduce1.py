"""
Implementation of map reduce algorithm using python built in functions
There will be 3 main elements to look at:
1. map
2. filter
3. reduce
"""


# 1. Map
# syntax: map(list_of_functions, list_of_inputs)

#### Squaring numbers ####
items = [1, 2 ,3, 4, 5]

# 1.a. Normal method

sqrd = []
for i in items:
    o = i**2
    sqrd.append(o)

# [1, 4, 9, 16, 25]
#print(sqrd)

# 1.b Map method
items = [1, 2 ,3, 4, 5]
sqrd = list(map(lambda x: x**2, items))
# print(sqrd)



# FILTER
# syntax: filter(function, items)
#### selecting items more or less than certain value ####
items = list(range(1, 11))

# 2.a. Normal method (list comprehension)
filtered = [i for i in items if i > 5]
# print(filtered)

# 2.b Filter method
filtered = list(filter(lambda x: x > 5, items))
# print(filtered)



# REDUCE
# syntax: reduce(list_of_funcs, list_of_items)

# cumulative computing of a list of num times a single number
# 1.a. Normal Method
product = 1
items = [1, 2, 3, 4, 5]
for i in items:
    product = product * i

# print(product)
# 120

# 1.b. Reduce Method
from functools import reduce
product = 1
product = reduce((lambda x, y: x * y), items)

# print(product)
