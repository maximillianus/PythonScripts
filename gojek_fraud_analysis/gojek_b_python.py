import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

## Import data
filename = 'gojek_problem_b.csv'
dataset = []
with open(filename, 'r') as f:
    lines = csv.reader(f)
    for row in lines:
        dataset.append(row)
    # alternative
    # dataset = list(lines)

print(dataset[0:3])
agentName = [d[0] for d in dataset[1:]]
timeStamp = [d[1] for d in dataset[1:]]
driverID = [d[2] for d in dataset[1:]]

## Questions to answer

# 1. How many driverID being registered for each agent?
from collections import Counter
counting = Counter(agentName)
print(counting)


"""
Ricky seems to have the most number of driver registered.
Mamat comes in second.
Bayu comes in 3rd.
"""

# 2. What is common registration period for each agent?

### let's first clean timestamp
from datetime import datetime
timeStamp = [t + '00' for t in timeStamp]
timeStamp = [datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f%z') for t in timeStamp]
timeStamp_date = [t.date() for t in timeStamp]
timeStamp_dayname = [t.date().strftime('%A') for t in timeStamp]
timeStamp_time = [t.time().strftime('%H:%M:%S') for t in timeStamp]
timeStamp_hour = [t[0:2] for t in timeStamp_time]
timeStamp_min = [t[3:5] for t in timeStamp_time]
timeStamp_sec = [t[7:10] for t in timeStamp_time]

# a. most common reg hours
hourCounter = Counter(timeStamp_hour)
#print(hourCounter)

dfhour = pd.DataFrame({'agent':agentName,
                       'hour':timeStamp_hour})

# shows frequency distribution of agentname vs hour
#print(pd.crosstab(index=dfhour.agent, columns=dfhour.hour))

# try to show top registration count and its hours
dfhour = dfhour.groupby(['agent', 'hour']).size().reset_index(name='count')
#print(dfhour.loc[dfhour.groupby(['agent'])['count'].idxmax()])

"""
- 4 out of 6 people commonly registers driver at 11AM
- 2 out of 6 people registers people the most at 11PM
- 11PM is way after working hours. Regist qty should not be high
"""

# b. try to check the registration days
dayorder = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday']

dfday = pd.DataFrame({'agent':agentName,
                      'date': timeStamp_date,
                      'dayname': timeStamp_dayname})
dfday.dayname = dfday.dayname.astype('category')
dfday.dayname.cat.reorder_categories(dayorder,inplace=True)

#print(dfday.head())
#print(pd.crosstab(index=dfday.agent, columns=dfday.dayname))

"""
Interestingly, Mamat & Ricky are registering drivers in weekends too!
Ricky has been registering agents at higher rate compared to his peer.
Mamat has been registering agents at much lower rate compared to his peer.
"""

# c. try to check time between registration.
# what is the registration duration?

# 3. Is there possible erroneous entry of driverID?

# let's look at some sample of driverID
#print('DriverID:', driverID[:5])
# driverID has 7 digits, started with '1' mostly.

# a. is there any wrong driverID?
#print('Check length of driverID')
errorlength = [[i,len(x)] for i,x in enumerate(driverID) if len(x) > 7]
# No length is beyond 7

# b. is there any funny driverID pattern?
# let's sort driverID for each agent and find if any ID is entered
# consecutively
dfdriver = pd.DataFrame({'agent': agentName,
                         'driverID': driverID})
print(dfdriver.head())


