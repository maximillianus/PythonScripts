import tkinter
import time #Header


print('HH:MM:SS')  # Output
print('--------')  # Output
#time definition

hour=int(0)
minz=int(0)
sec=int(5)

while hour > -1:
    while minz > -1:
        while sec > 0:
         sec=sec-1
         time.sleep(1)
         sec1 = ('%02.f' % sec)
         min1 = ('%02.f' % minz)
         hour1 = ('%02.f' % hour)
         print ('\r' + str(hour1) + ":" + str(min1) + ":" + str(sec1))
        minz=minz-1
        sec=60
        hour=hour-1
    minz=59


print('Session ended.')



