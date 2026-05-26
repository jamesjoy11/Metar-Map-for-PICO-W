import lanconnect
import ntptime
from time import sleep
import time
import metarmap
import machine

#DO NOT Modify anything above this Line!!!!!!!

#Enter your Time Preferences
MORNING_ON = 7   						#Time to turn on display in morning, 24 hour clock
EVENING_OFF = 22						#Time to turn off display at night, 24 hour clock
TIMEZONEOFFSET = -5  					#Your Timezone offset from UTC


#DO NOT Modify anything below this Line!!!!!!!
ntptime.settime()

with open("airports") as f:
    airports = f.readlines()
airports = [x.strip() for x in airports]
f.close
j=0
errorcounter = 0
while (True):
    currenthour = (time.localtime()[3]) + TIMEZONEOFFSET
    if currenthour < 0: currenthour = currenthour +24
    if currenthour > 24: currenthour = currenthour - 24
    print ("current Hour",currenthour)
    if (currenthour) > MORNING_ON and (currenthour) < EVENING_OFF:
        if lanconnect.checkconnection():
            try:
                 metarmap.metar(airports)
            except:
                print ("couldn't Get Data from weather.gov")
                errorcounter = errorcounter + 1
              
            else:
                print("Running weather loop Script")
        else:
            sleep(30)
            lanconnect.connect()
    else:
        print(time.localtime(), 'sleeping  Count ',j)
        metarmap.lightsout()
        sleep(300)
        j=j+1
        if j > 536870912:
            j=0
    if errorcounter > 20:
        machine.reset()
    

