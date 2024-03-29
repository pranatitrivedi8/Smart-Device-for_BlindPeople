from sense_hat import SenseHat
from datetime import datetime
import sys
from time import sleep
from evdev import InputDevice, ecodes, list_devices
from select import select
import logging
import gps
count=0
# Listen on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

# Use the logging library to handle all our data recording
logfile = "gravity-"+str(datetime.now().strftime("%Y%m%d-%H%M"))+".csv"
# Set the format for the timestamp to be used in the log filename
logging.basicConfig(filename=logfile, level=logging.DEBUG,
    format='%(asctime)s %(message)s')

def gentle_close(): # A function to end the program gracefully
        sh.clear(255,0,0) # Turn on the LEDs red
        sleep(0.5) # Wait half a second
        sh.clear(0,0,0) # Turn all the LEDs off
        sys.exit() # Quit the program

sh = SenseHat() # Connect to SenseHAT
sh.clear() # Turn all the LEDs off
# Find all the input devices connect to the Pi
devices=[InputDevice(fn) for fn in list_devices()]
for dev in devices:
    # Look for the SenseHAT Joystick
    if dev.name=="Raspberry Pi Sense HAT Joystick":
        js=dev
# Create a variable to store whether or not we're logging data
running = True # No data being recorded (yet)
try:
    print('Press the Joystick button to start recording.')
    print('Press it again to stop.')
    while True:
        # capture all the relevant events from joystick
        #r,w,x=select([js.fd],[],[],0.01)
        #for fd in r:
         #   for event in js.read():
                # If the event is a key press...
          #      if event.type==ecodes.EV_KEY and event.value==1:
                    # If we're not logging data, start now
                    #if event.code==ecodes.KEY_ENTER and not running:
                        #running = True # Start recording data
                        #sh.clear(0,255,0) # Light up LEDs green
                    # If we were already logging data, stop now
                    #elif event.code==ecodes.KEY_ENTER and running:
                        #running = False
                        #gentle_close()
        # If we're logging data...
        if running:
               # Read from acceleromter
            acc_x,acc_y,acc_z = [sh.get_accelerometer_raw()[key] for key in ['x','y','z']]
            # Format the results and log to file
            logging.info('{:12.10f}, {:12.10f}, {:12.10f}'.format(acc_x,acc_y,acc_z))
            print(acc_x,acc_y,acc_z) # Also write to screen
            if acc_x<0.05 and acc_x>-0.05 and acc_y<0.05 and acc_y>-0.05 and acc_z<0.3 and acc_z>-0.0:
                print('fall detected')
                #datafile=acc_x,acc_y,acc_z,report
                filee=str('fall detect')
                f=open('/home/pi/Desktop/Project442/peoplestatus.txt','a')
                f.write(filee+'\n\n')
                count = count + 1

                while count==1:
                        try:
                            report = session.next()
                            # Wait for a 'TPV' report and display the current time
                            # To see all report data, uncomment the line below
                            print(report)
                            fileee=str(report)
                            f=open('/home/pi/Desktop/Project442/peoplestatus.txt','a')
                            f.write(fileee+'\n\n')

                            if report['class'] == 'TPV':
                                if hasattr(report, 'time'):
                                    print(report.time)
                                    count = count + 1
#                                    datafile=acc_x,acc_y,acc_z,report
#                                    filee=str(datafile)
#                                    f=open('/home/pi/data.txt','a')
#                                    f.write(filee+'\n\n')

				  #gentle_close()
                                    if count==2:
                                       #quit()
                                       #datafile=acc_x,acc_y,acc_z,report
                                       fileeee=str(report)
                                       f=open('/home/pi/Desktop/Project442/peoplestatus.txt','a')
                                       f.write(fileeee+'\n\n')

                                       count = count + 1
                                       if count==3:
                                           quit()

                        except KeyError:
                               pass
                        except KeyboardInterrupt:
                               quit()
                        except StopIteration:
                               session = None

                        #print("GPSD has terminated")

                #datafile=acc_x,acc_y,acc_z,report
                #filee=str(datafile)
                #f=open('/home/pi/data.txt','a')
                #f.write(filee+'\n\n')

              #filee=str('fall detected',report)
              #f=open('/home/pi/data.txt','a')
              #f.write(filee+'\n\n')

except: # If something goes wrong, quit
    gentle_close()
