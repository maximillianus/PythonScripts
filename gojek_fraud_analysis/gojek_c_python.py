import os
import csv
import pandas as pd
import datetime
import math

print(os.getcwd())

## Functions
def get_distance(lat_1, lng_1, lat_2, lng_2): 
    d_lat, d_lng = (lat_2 - lat_1), (lng_2 - lng_1) 
    temp = math.sin(d_lat / 2)**2 + math.cos(lat_1) * math.cos(lat_2) * math.sin(d_lng / 2)**2

    return 6371.0 * (2 * math.atan2(math.sqrt(temp), math.sqrt(1 - temp)))

## Read data
filename = 'gojek_problem_c.csv'
df = pd.read_csv(filename)


## Data Cleaning

# convert integer to date for data_date
df.data_date = [int(i) for i in df.data_date]
df.data_date = [(datetime.datetime(1899,12,30) + datetime.timedelta(days=int(t))) for t in df.data_date]

# convert booking_date, dispatch_time, closing_time to datetime object
df.booking_date = [pd.to_datetime(t).tz_localize('UTC').tz_convert('Asia/Jakarta') for t in df.booking_date]
df.dispatch_time = [pd.to_datetime(t).tz_localize('UTC').tz_convert('Asia/Jakarta') for t in df.dispatch_time]

# When converting dispatch time to closing time, there is unusual datetime pattern observed
# observed 24:16:10 instead of 00:16:10. Need to investigate further on this

# ** unusual closing_time format **
unusual_closing_time_format = [ [i, t[11:19]] for i, t in enumerate(df.closing_time) if t[11:13] == '24']
print(unusual_closing_time_format)

# format to correct one
df.closing_time = [t.replace(' 24:',' 00:') for t in df.closing_time]
df.closing_time = [pd.to_datetime(t).tz_localize('UTC').tz_convert('Asia/Jakarta') for t in df.closing_time]

## Clean leading/trailing whitespace
df.customer_name = df.customer_name.str.strip()
df.driver_name = df.driver_name.str.strip()
df.destination_address = df.destination_address.str.strip()



## Investigation

# Check how many booking/dispatch/closing per date
df.booking_date.dt.strftime('%Y-%m-%d').value_counts(sort=False).sort_index()
df.dispatch_time.dt.strftime('%Y-%m-%d').value_counts(sort=False).sort_index()
df.closing_time.dt.strftime('%Y-%m-%d').value_counts(sort=False).sort_index()

# Check how many booking/dispatch/closing per time
df.booking_date.dt.strftime('%H-%M-00').value_counts(sort=False).sort_index()
df.dispatch_time.dt.strftime('%H-%M-00').value_counts(sort=False).sort_index()
df.closing_time.dt.strftime('%H-%M-00').value_counts(sort=False).sort_index()

# Check time difference between book - dispatch
# ** There is a lot of booking dispatched within 5 seconds or less
book_to_dispatch = df.dispatch_time - df.booking_date
print(book_to_dispatch.value_counts().head(10))

# Check time difference between dispatch - close
# ** There is a lot of booking closed within 20 seconds or less
# ** It does not make sense booking can be closed within seconds
# but probably there is short distance
dispatch_to_close = df.closing_time - df.dispatch_time
print(dispatch_to_close.value_counts().head(10))

df['book_to_dispatch'] = book_to_dispatch
df['dispatch_to_close'] = dispatch_to_close
df['book_to_close'] = book_to_dispatch + dispatch_to_close

# Check the distance
df.origin_lat_rad = [math.radians(geo) for geo in df.origin_latitude]
df.origin_lon_rad = [math.radians(geo) for geo in df.origin_longitude]
df.destination_lat_rad = [math.radians(geo) for geo in df.destination_latitude]
df.destination_lon_rad = [math.radians(geo) for geo in df.destination_longitude]


print(get_distance(df.origin_lat_rad[0], df.origin_lon_rad[0],
    df.destination_lat_rad[0], df.destination_lon_rad[0]))

geolist = [[i,j,k,l] for i,j,k,l in zip(df.origin_latitude, df.origin_longitude, 
   df.destination_latitude, df.destination_longitude)]

geolist_rad = [[math.radians(i) for i in geo] for geo in geolist ]

df['calc_distance'] = [get_distance(geo[0], geo[1], geo[2], geo[3]) for geo in geolist_rad  ]



## Observation & Analysis
print("** Observation & Analysis **")

# within 1 week, there are 197 completed booking under the driver HARRY
# All done in period of 8-9 Apr 2017 11PM - 2AM
print(df.driver_name.value_counts().head(10))
print(df[df.driver_name == 'HARRY'].booking_date.min())
print(df[df.driver_name == 'HARRY'].booking_date.max())

# Time to close booking is between 16secs - 3min:38secs
# Distance covered is 16 - 25miles
print(df[df.driver_name == 'HARRY'].book_to_close.describe())
print(df[df.driver_name == 'HARRY'].total_distance.describe())

# Check distribution of destination address
print(df[df.driver_name == 'HARRY'].destination_address.value_counts())


# Check customer name
print(df[df.driver_name == 'HARRY'].customer_name.value_counts())
# wita, yanti, son, ani, sanah, yani, hasan, fina

# Is this regular customer? check whether they are ordering on other date
harry_customerlist = df[df.driver_name == 'HARRY'].customer_name.unique()
print(df[df.customer_name.isin(harry_customerlist)].booking_date.dt.date.unique())
# these customers are only booking at this specific date ie 8-9 Apr.
# Based on irregularities on temporal-spatial (time-distance) aspects, as well as 
# booking period, and customer name, it is highly likely that this is a fraud.

# Patterns observed:
# - Volume of order
# - Logistic agents ie. driver
# - Customer
# - booking period
# - time taken to complete a booking
# - distance traveled


## Additional Analysis 
# First subset the data from those with HARRY as driver
df2 = df.loc[df[df.driver_name != 'HARRY'].index]

# Check daily number of booking
# higher order volume on 4th & 7th
print(df2.booking_date.dt.date.value_counts().sort_index(ascending=False))

# Check driver list
# 38 unique names. Surdi takes highest order at 4
print(df2.driver_name.nunique())
print(df2.driver_name.value_counts())

# Check customer name list
# 38 unique names. 'hana' & 'agung' is the top
print(df2.customer_name.nunique())
print(df2.customer_name.value_counts())

# Check book to close time
# min at 8mins, max at 2 hours 30 mins, median at 26mins
print(df2.book_to_close.describe())
# max: 2 hours 30 min due to 1 hour book and 1 hour travel time
# suspect probably first-time customer
# min: 8 min due to short distance 

# Check distance statistics
# mean at 3.76km, max at 14km, min at 0.46km, median at 3.1km
print(df2.total_distance.describe())
# compare total distance again distance calc from lon-lat

# Check destination address:
# top address is jalan raya ciangsana at bogor at 6 counts
print(df2.destination_address.value_counts().head(5))
# mostly to customer named agung, daily order at morning.
# the other 2 is night-call





