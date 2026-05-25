import network
from time import sleep
import machine
import urequests

#Do NOT Modify anything Above this line!!!!

#Enter your WiFi settings
hostname = "picometarmap"		#Hostname to find your Metar Map on your local WiFi network
ssid = 'YourNetwork'				#Your Local WiFi Network SSID
password = 'YourPassword'			#Your Local WiFi Network Password

#Do NOT Modify anything Below this line!!!!

led_onboard = machine.Pin("LED", machine.Pin.OUT)
led_onboard.off()
network.hostname(hostname)
wlan = network.WLAN(network.STA_IF)
connectionstatus = False

def connect():
    #Connect to WLAN
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    led_onboard.on()

def checkconnection():
    connectionstatus = wlan.isconnected()
    if connectionstatus == False:
        led_onboard.off()
    return connectionstatus    
         
          