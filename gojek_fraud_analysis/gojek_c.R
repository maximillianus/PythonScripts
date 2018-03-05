## Go-jek Problem C ##

require(dplyr)
require(ggplot2)
require(geosphere)

setwd("C:/NotBackedUp/datafiles/others")
getwd()

## Import data
df <- read.csv('gojek_problem_c.csv',stringsAsFactors = F)
str(df)

## Data cleaning
# data date
df$data_date <- as.Date(df$data_date, origin = '1899-12-30')

# booking_date
df$booking_date <- strptime(df$booking_date, format='%Y-%m-%d %H:%M:%OS', tz='Asia/Jakarta')

# dispatch_time
df$dispatch_time <- strptime(df$dispatch_time, format='%Y-%m-%d %H:%M:%OS', tz='Asia/Jakarta')

# closing_time
df$closing_time <- strptime(df$closing_time, format='%Y-%m-%d %H:%M:%OS', tz='Asia/Jakarta')


## Data transformation
# Book to dispatch duration

# booking duration
book_duration <- df$closing_time - df$dispatch_time

## Data exploration
# Check shape
dim(df)

# Quick summary
summary(df)
