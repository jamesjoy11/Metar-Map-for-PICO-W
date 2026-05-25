# Metar-Map-for-PICO-W
Ported the Metar Map from Phillip Reuker to run on a PICO W

I took the Code from Pillip Reuker's metar Map and ported it over the Raspberry Pi PICO W.  Since it does not have an OS, it took an extensive amount of rewriting and error handling.  I hope I have figured out most of the potential problems.
I will not recount the entire build process, but I will explain how to install and connect to the PICO Pi.  
You will need to install Thonny and configure for your computer. No SSH need.  You will need a micro USB cable to connect to your computer.   
Obviously download all of the files put in your local directory.  First edit the lanconnect.py to input your nework paramters.  You can also change the hostname if your prefer.  Next put in a list of the airports in the airports file.  Note, no file extension so you will need to do this in notepad or some text editor.  Next, if you need to or prefer, edit the items in the metarmap.py file.  This would be preferences for the colors, wind, etc.  You may also need to change the RGB order for your type of LEDs.  Finally, you will need to edit the main.py for your timezone offset and on/off preferences for going dark at night.

After you get all of this ready, you can connect your pico, but make sure it has micropython loaded.  If it does not yet, you will need to do so.  There is lots of online help if you need it.  After, connect your pico pi to your computer with the USB cable and in Thonny go to configure interpreter.  Again, lots of online help if needed.
At this point, transfer all of the files.  

Next, connect your plug power for the LEDs to VBUS pin, Negative to GND and signal to GP0.  After plugging in your LEDs, connect Power from a micro USB USB power supply and everything should come on and you should have weather.  

If things don't work, you can connect back to your computer and from Thonny type CTL-C or click STOP until you have control, and trouble shoot.

