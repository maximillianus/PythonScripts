import os
import csv

## Import data
filename = 'gojek_problem_b.csv'
dataset = []
with open(filename, 'r') as f:
    lines = csv.reader(f)
    dataset = list(lines)
    # lines = f.readlines()
    # lines = [l.replace('\n', '') for l in lines]
    # dataset = (lines)

print(dataset[0:3])
agentName = [d[0] for d in dataset[1:]]
timeStamp = [d[1] for d in dataset[1:]]
driverID = [d[2] for d in dataset[1:]]

## Questions to answer

# How many driverID being registered for each agent?
from collections import Counter
counting = Counter(agentName)
print(counting)

"""
Ricky seems to have the most number of driver registered.
Mamat comes in second.
Bayu comes in 3rd.
"""

# What is common registration period for each agent?

### let's first clean timestamp
from datetime import datetime
timeStamp = [t + '00' for t in timeStamp]
timeStamp = [datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f%z') for t in timeStamp]
timeStamp_date = timeStamp[0].date()
print(type(timeStamp_date))

