import os
import sys
from random import choice
from datetime import datetime
import time


# Set home dir
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(basedir)


# Validate KaizenKamp folder and the userlist files
folderloc = '\\datafiles\\KaizenKampHost\\'
if(not os.path.isdir(basedir+folderloc)):
	print(basedir+folderloc, "does not exist. Please create directory.")
	quit()

filehost = "Users_host.txt"
#filetoast = "Users_toastmaster.txt"
filealgo = "Users_algorithm.txt"

if(not os.path.exists(basedir+folderloc+filehost)):
	print(filehost, "does not exist. Please create the file.")
	quit()
# if(not os.path.exists(basedir+folderloc+filetoast)):
# 	print(filetoast, "does not exist. Please create the file.")
# 	quit()
if(not os.path.exists(basedir+folderloc+filealgo)):
	print(filealgo, "does not exist. Please create the file.")
	quit()

# Make a list of users for host, toastmaster, algorithm
file = open(basedir+folderloc+filehost, 'r')
usernames_host = file.read().splitlines()
# file = open(basedir+folderloc+filetoast, 'r')
# usernames_toastmaster = file.read().splitlines()
file = open(basedir+folderloc+filealgo, 'r')
usernames_algorithm = file.read().splitlines()

# Randomly pick 1 user

## Display randomizer just for fun
sys.stdout.write('\rRandomizing')
sys.stdout.flush()
time.sleep(0.4)
sys.stdout.write('\rRandomizing.')
sys.stdout.flush()
time.sleep(0.4)
sys.stdout.write('\rRandomizing..')
sys.stdout.flush()
time.sleep(0.4)
sys.stdout.write('\rRandomizing...\n')
sys.stdout.flush()
time.sleep(0.4)

# import time
# for x in range (0,5):  
#     b = "Randomizing" + "." * x
#     print (b, end="\r")
#     time.sleep(1)

#Host
c_host = choice(usernames_host)
while(c_host == 'Abhijit Bhonsle'):
	c_host = choice(usernames_host)
print("Host:", c_host)
usernames_host.remove(c_host)
#Toastmaster
# c_toastmaster = choice(usernames_toastmaster)
# while(c_toastmaster == c_host):
# 	c_toastmaster = choice(usernames_toastmaster)
# print("ToastMaster:",c_toastmaster)
# usernames_toastmaster.remove(c_toastmaster)
#Algorithm
c_algorithm = choice(usernames_algorithm)
# while(c_algorithm == c_host or c_algorithm == c_toastmaster):
while(c_algorithm == c_host or c_algorithm == 'Abhijit Bhonsleb'):
	c_algorithm = choice(usernames_algorithm)
print("Algorithm:",c_algorithm)
usernames_algorithm.remove(c_algorithm)

# Write remaining users into the same file
file = open(basedir+folderloc+'Users_host.txt','w')
for user in usernames_host:
	file.write("%s\n" % user)

# file = open(basedir+folderloc+'Users_toastmaster.txt','w')
# for user in usernames_toastmaster:
# 	file.write("%s\n" % user)

file = open(basedir+folderloc+'Users_algorithm.txt','w')
for user in usernames_algorithm:
	file.write("%s\n" % user)

# Write appeared users into different file
today = datetime.today().strftime("%Y-%m-%d")

file = open(basedir+folderloc+'Users_host_appeared.txt','a')
file.write("%s\n" % (c_host+' - '+today))
# file = open(basedir+folderloc+'Users_toastmaster_appeared.txt','a')
# file.write("%s\n" % (c_toastmaster+' - '+today))
file = open(basedir+folderloc+'Users_algorithm_appeared.txt','a')
file.write("%s\n" % (c_algorithm+' - '+today))

# Close opened files
file.close()