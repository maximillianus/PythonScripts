## Go-jek problem B ##
require(dplyr)

setwd("C:/NotBackedUp/datafiles/others")
getwd()


## Read data
df <- read.csv('gojek_problem_b.csv', stringsAsFactors = F)
str(df)
head(df)

## Data cleaning & transformation
names(df) <- c('AgentName', 'Timestamp', 'DriverID')

# Date
dates <- sapply(strsplit(df$Timestamp, split=' '), '[[', 1)
df$Date <- dates

# Time
times <- sapply(strsplit(df$Timestamp, split=' '), '[[', 2)
df$Times <- times

# Hour
hours <- paste0(substr(times, 1,3), '00:00')
df$Hour <- hours


#x <- df[1,2]
#xdatetime <- strptime(x, format='%Y-%m-%d %H:%M:%OS%z', tz='UTC')
#xdatetime


## Data exploration
require(ggplot2)

# DF Shape
print('Shapes of df:')
dim(df)

print('Unique DriverID:')
length(unique(df$DriverID))

print('Registration / Date:')
table(df$Date)

print('Registration / Agent:')
table(df$AgentName)

## Let's look at distribution of agent registration versus Date
print('Date ~ Agent Registration')
#(table(df$AgentName, df$Date))
df_agentdate <- df %>% group_by(Date, AgentName) %>% summarise(n=n())
df_agentdate
ggplot(data=df_agentdate, aes(x=Date, y=n, group=AgentName, colour=AgentName)) + 
  geom_line(size=1.0)+
  geom_point(size=1.5)

# from the plot we can observe that Mamat & Ricky has different trends 
# compared to the rest of the agents.

# Mamat is constantly registering low number of drivers but it spikes up
# during weekend ie. 13-14 May '17.

# Ricky has erratic trend in agent registration. He registers abnormally high
# number of drivers at times when other agents are registering low number.
# He also registers drivers on non-working days ie. 13-14 May '17.

## Let's look at distribution of agent registration qty versus hour
## Take the mean
print('Date ~ Agent Registration')
#(table(df$AgentName, df$Date))
df_agenthour <- df %>% group_by(Date, Hour, AgentName) %>% summarise(n=(n())) %>% 
  ungroup() %>% group_by(AgentName, Hour) %>% summarise(mean=mean(n))
df_agenthour
ggplot(data=df_agenthour, aes(x=Hour, y=mean, group=AgentName, colour=AgentName)) + 
  geom_line(size=1.0)+
  geom_point(size=1.5)


