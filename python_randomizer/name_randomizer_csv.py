import time
import os
import sys

print("#### STARTING RANDOMIZER! ####")
time.sleep(0.5)

print()
for i in range(0,4):
    #sys.stdout.write("\033[K")
    print("Initializing"+"."*i, end="\r")
    #print(i, end="\r")
    time.sleep(0.3)
print()

import pandas as pd
import numpy as np
from datetime import datetime
import colorama
colorama.init()


# Set home dir
basedir = os.path.dirname(os.path.abspath(__file__))
#print(basedir)

# Validate KaizenKamp folder and the userlist files
# folderloc = '\\datafiles\\KaizenKampHost\\'
# if(not os.path.isdir(basedir+folderloc)):
# 	print(basedir+folderloc, "does not exist. Please create directory.")
# 	quit()

fileName = "\\namelist.csv"
if(not os.path.exists(basedir+fileName)):
	print(filehost, "does not exist. Please create the file.")
	quit()

# Make a list of users for host, toastmaster, algorithm
usernames = pd.read_csv(basedir+fileName, dtype=object)
#print(usernames.info())

# Randomly choice person for host, toastmaster, algorithm
c_host = usernames.Host.dropna().sample().to_string(index=False)
c_toast = usernames.Toast.dropna().sample().to_string(index=False)
while(c_toast == c_host):
	c_toast = usernames.Toast.dropna().sample().to_string(index=False)
c_algo = usernames.Algorithm.dropna().sample().to_string(index=False)
while(c_algo == c_host or c_algo == c_toast):
	c_algo = usernames.Algorithm.dropna().sample().to_string(index=False)

# Rolling randomizer
for i in range(0,80):
	c = usernames.Host.dropna().sample().to_string(index=False)
	print('KaizenKamp Host is: '+ '\033[K' + c, end='\r', flush=True)
	time.sleep(0.03)
print("KaizenKamp Host is: "+'\033[K'+c_host)

input("Next?")

for i in range(0,80):
	c = usernames.Toast.dropna().sample().to_string(index=False)
	print('Toastmaster Host is: '+ '\033[K' + c, end='\r', flush=True)
	time.sleep(0.03)
print("Toastmaster Host is: "+'\033[K'+c_toast)

input("Next?")

for i in range(0,80):
	c = usernames.Algorithm.dropna().sample().to_string(index=False)
	print('Algorithm Host is: '+ '\033[K' + c, end='\r', flush=True)
	time.sleep(0.03)
print("Algorithm Host is: "+'\033[K'+c_algo)

input("Happy with the selection?")

print()
for i in range(0,4):
    #sys.stdout.write("\033[K")
    print("Recording result"+"."*i, end="\r")
    #print(i, end="\r")
    time.sleep(0.35)

# Appending to Appeared List
if(usernames.HostAppeared.last_valid_index() == None ):
	usernames.set_value(0,'HostAppeared',c_host)
else:
	n = usernames.HostAppeared.last_valid_index()
	usernames.set_value(n+1,'HostAppeared',c_host)
	
if(usernames.AlgorithmAppeared.last_valid_index() == None ):
	usernames.set_value(0,'AlgorithmAppeared',c_algo)
else:
	n = usernames.AlgorithmAppeared.last_valid_index()
	usernames.set_value(n+1,'AlgorithmAppeared',c_algo)

if(usernames.ToastmasterAppeared.last_valid_index() == None ):
	usernames.set_value(0,'ToastmasterAppeared',c_toast)
else:
	n = usernames.ToastmasterAppeared.last_valid_index()
	usernames.set_value(n+1,'ToastmasterAppeared',c_toast)

# Adding Date
today = datetime.today().strftime("%Y-%m-%d")
#todaySeries = pd.Series([today])
if(usernames.Date.last_valid_index() == None ):
	usernames.set_value(0,'Date',today)
else:
	n = usernames.Date.last_valid_index()
	usernames.set_value(n+1,'Date',today)


# Removing from Remaining List
usernames.Host.replace(c_host, np.NaN, inplace=True)
usernames.Algorithm.replace(c_algo, np.NaN, inplace=True)
usernames.Toast.replace(c_toast, np.NaN, inplace=True)

print()
for i in range(0,4):
    #sys.stdout.write("\033[K")
    print("Writing to File"+"."*i, end="\r")
    #print(i, end="\r")
    time.sleep(0.35)

# Write back into csv file
usernames.to_csv(basedir+'\\namelist.csv', index=False)


print()
print("#### Thanks for participating! ####")