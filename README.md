# Metar-Map-for-PICO-W
Ported the Metar Map from Phillip Reuker to run on a PICO W

I took the Code from Pillip Reuker's metar Map and ported it over the Raspberry Pi PICO W.  Since it does not have an OS, it took an extensive amount of rewriting and error handling.  I hope I have figured out most of the potential problems.
I will not recount the entire build process, but I will explain how to install and connect to the PICO Pi.  
You will need to install Thonny and configure for your computer. No SSH need.  You will need a micro USB cable and connect to your computer.   
Obviously download all of the files put in your local directory.  First edit the lanconnect.py to input your nework paramters.  You can also change the hostname if your prefer.  Next put in a list of the airports in the airports file.  Note, no file extension so you will need to do this in notepad or some text editor.  Next, if you need to or prefer, edit the items in the metarmap.py file.  This would be preferences for the colors, wind, etc.  You may also need to change the RGB order for your type of LEDs.  Finally, you 
