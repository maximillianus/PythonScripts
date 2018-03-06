import os
import csv
import pandas as pd
import datetime

print(os.getcwd())

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

