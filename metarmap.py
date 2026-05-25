import lanconnect
import xmllib
import urequests
from neopixel import Neopixel
from xmllib import xmlfind
from time import sleep
import time

#DO NOT Modify Anything above this line

# NeoPixel LED Configuration
LED_COUNT			= 30				# Number of LED pixels.
LED_PIN				= 0					# GPIO pin connected to the pixels 
LED_BRIGHTNESS		= 50				# Int from 50 (min) to 100 (max)
LED_ORDER			= 'GRB'				# Strip type and colour ordering

COLOR_VFR			= (255,0,0)			# Green
COLOR_VFR_FADE		= (125,0,0)			# Green Fade for wind
COLOR_MVFR			= (0,0,255)	    	# Blue
COLOR_MVFR_FADE		= (0,0,125)			# Blue Fade for wind
COLOR_IFR			= (0,255,0)			# Red
COLOR_IFR_FADE		= (0,125,0)			# Red Fade for wind
COLOR_LIFR			= (0,125,125)		# Magenta
COLOR_LIFR_FADE		= (0,75,75)			# Magenta Fade for wind
COLOR_CLEAR			= (0,0,0)			# Clear
COLOR_LIGHTNING		= (255,255,255)		# White
COLOR_HIGH_WINDS 	= (255,255,0) 		# Yellow

# ----- Blink/Fade functionality for Wind and Lightning -----
# Do you want the METARMap to be static to just show flight conditions, or do you also want blinking/fading based on current wind conditions
ACTIVATE_WINDCONDITION_ANIMATION = True	# Set this to False for Static or True for animated wind conditions
#Do you want the Map to Flash white for lightning in the area
ACTIVATE_LIGHTNING_ANIMATION = True		# Set this to False for Static or True for animated Lightning
# Fade instead of blink
FADE_INSTEAD_OF_BLINK	= False			# Set to False if you want blinking
# Blinking Windspeed Threshold
WIND_BLINK_THRESHOLD= 15				# Knots of windspeed to blink/fade
HIGH_WINDS_THRESHOLD= 25				# Knots of windspeed to trigger Yellow LED indicating very High Winds, set to -1 if you don't want to use this
ALWAYS_BLINK_FOR_GUSTS = True			# Always animate for Gusts (regardless of speeds)
# Blinking Speed in seconds
BLINK_SPEED		= 1						# Int in seconds
BLINK_TOTALTIME_SECONDS	= 300			# Time between refreshes from the Aviation Weather website


#Do NOT Modify Anthing below this Line!!!!!!

pixels = Neopixel(LED_COUNT, LED_PIN, 0, LED_ORDER)
pixels.brightness(LED_BRIGHTNESS)

def metar(airports):
    url = "https://www.aviationweather.gov/api/data/metar?ids=" + ",".join([item for item in airports if item != "NULL"]) + "&format=xml&mostRecentForEachStation=postfilter"

    j=0
    try:
        response = urequests.get(url)
    except:
        print ("couldn't Get Data from weather.gov")
        sleep(15)
    else:
        print("Got Weather Data")
        res = response.text
        response.close
            
    start =0
    conditionDict = { "NULL": {"flightCategory" : "", "windSpeed" : 0, "windGustSpeed" :  0, "windGust" : False, "lightning": False } }
    conditionDict.pop("NULL")
    stationList = []
    j=0
    windSpeed = 0
    windGustSpeed = 0
    windGust = False
    lightning = False       
    xb = res.find('<data num_results="') + len('<data num_results="')
    xe = res.find('">',xb)
    num_results = int(res[xb:xe])
    for i in range (num_results):	
        start = res.find('<METAR>',start)
        end = res.find('</METAR>',start)
        stationId = xmlfind('station_id',res,start,end)
        rawText = xmlfind ('raw_text',res, start,end)
        lightning = False
        if rawText.find('LTG') >0 or rawText.find('TS') >0 :
            lightning = True   
        flightCategory = xmlfind('flight_category',res, start,end)
        windSpeed = xmlfind('wind_speed_kt', res, start,end)
        windGustSpeed = xmlfind('wind_gust_kt', res, start,end)
        windGust = (True if ((ALWAYS_BLINK_FOR_GUSTS and int(windGustSpeed) > 0) or int(windGustSpeed) > WIND_BLINK_THRESHOLD) else False)
        start = end + 6
        conditionDict[stationId] = { "flightCategory" : flightCategory, "windSpeed" : windSpeed, "windGustSpeed": windGustSpeed, "windGust": windGust, "lightning": lightning }
        stationList.append(stationId)
    looplimit = int(round(BLINK_TOTALTIME_SECONDS / BLINK_SPEED)) if (ACTIVATE_WINDCONDITION_ANIMATION or ACTIVATE_LIGHTNING_ANIMATION or ACTIVATE_EXTERNAL_METAR_DISPLAY) else 1
    windCycle = False
    displayTime = 0.0
    displayAirportCounter = 0
    numAirports = len(stationList)
    while looplimit > 0:
        i = 0
        for airportcode in airports:
            # Skip NULL entries
            if airportcode == "NULL":
                i += 1
                continue
            color = COLOR_CLEAR
            conditions = conditionDict.get(airportcode, None)
            windy = False
            highWinds = False
            lightningConditions = False
            windblink = False
                
            if conditions != None:
                windy = True if (ACTIVATE_WINDCONDITION_ANIMATION and windCycle == True and (int(conditions["windSpeed"]) >= WIND_BLINK_THRESHOLD or conditions["windGust"] == True)) else False
                highWinds = True if (windy and HIGH_WINDS_THRESHOLD != -1 and (int(conditions["windSpeed"]) >= HIGH_WINDS_THRESHOLD or int(conditions["windGustSpeed"]) >= HIGH_WINDS_THRESHOLD)) else False
                lightningConditions = True if (ACTIVATE_LIGHTNING_ANIMATION and windCycle == False and conditions["lightning"] == True) else False
                if conditions["flightCategory"] == "VFR":
                    color = COLOR_VFR if not (windy or lightningConditions) else COLOR_LIGHTNING if lightningConditions else COLOR_HIGH_WINDS if highWinds else (COLOR_VFR_FADE if FADE_INSTEAD_OF_BLINK else COLOR_CLEAR) if windy else COLOR_CLEAR
                elif conditions["flightCategory"] == "MVFR":
                    color = COLOR_MVFR if not (windy or lightningConditions) else COLOR_LIGHTNING if lightningConditions else COLOR_HIGH_WINDS if highWinds else (COLOR_MVFR_FADE if FADE_INSTEAD_OF_BLINK else COLOR_CLEAR) if windy else COLOR_CLEAR
                elif conditions["flightCategory"] == "IFR":
                    color = COLOR_IFR if not (windy or lightningConditions) else COLOR_LIGHTNING if lightningConditions else COLOR_HIGH_WINDS if highWinds else (COLOR_IFR_FADE if FADE_INSTEAD_OF_BLINK else COLOR_CLEAR) if windy else COLOR_CLEAR
                elif conditions["flightCategory"] == "LIFR":
                    color = COLOR_LIFR if not (windy or lightningConditions) else COLOR_LIGHTNING if lightningConditions else COLOR_HIGH_WINDS if highWinds else (COLOR_LIFR_FADE if FADE_INSTEAD_OF_BLINK else COLOR_CLEAR) if windy else COLOR_CLEAR
                else:
                    color = COLOR_CLEAR
                
            print("Setting LED " + str(i) + " for " + airportcode + " to " + ("lightning " if lightningConditions else "") + ("very " if highWinds else "") + ("windy " if windy else "") + (conditions["flightCategory"] if conditions != None else "None") + " " + str(color))
            pixels.set_pixel(i,color)
            i += 1		
        pixels.show()
        sleep(BLINK_SPEED)
        windCycle = False if windCycle else True
        looplimit -= 1
        if looplimit < 1 : print(time.localtime(),"looplimit", str(color))
        
def lightsout():
    pixels.fill(COLOR_CLEAR)
    pixels.show()
 