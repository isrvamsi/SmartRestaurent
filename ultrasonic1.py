#!/usr/bin/python
import signal
import sys
import time
import RPi.GPIO as GPIO
from display import TM1637

THRESHOULD1 = 80
THRESHOULD2 = 80

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
# Define GPIO to use on Pi
GPIO_TRIGGER1 = 23
GPIO_ECHO1    = 24
GPIO_TRIGGER2 = 17
GPIO_ECHO2    = 27

print "Ultrasonic Measurement"

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER1,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_TRIGGER2,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO1,GPIO.IN)      # Echo
GPIO.setup(GPIO_ECHO2,GPIO.IN)      # Echo


def signal_handler(signal, frame):
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


#Variables for people count
time1 = 0
time2 =0
sensor1 = False
sensor2 = False
people =0
#"""Confirm the display operation"""
display = TM1637(CLK=21, DIO=20, brightness=1.0)
display.Clear()

digits = [1, 2, 3, 4]
display.Show(digits)
time.sleep(3)

display.Clear()

#Init complete
while True:
  
  # Set trigger to False (Low)
  GPIO.output(GPIO_TRIGGER1, False)

  # Allow module to settle
  time.sleep(0.001)

  # Send 10us pulse to trigger
  GPIO.output(GPIO_TRIGGER1, True)
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER1, False)
  start1 = time.time()

  while GPIO.input(GPIO_ECHO1) == 0:
    start1 = time.time()

  while GPIO.input(GPIO_ECHO1) == 1:
    stop1 = time.time()

  # Calculate pulse length
  elapsed1 = stop1 - start1

  # Distance pulse travelled in that time is time
  # multiplied by the speed of sound (cm/s)
  distance1 = elapsed1 * 34300

  # That was the distance there and back so halve the value
  distance1 = distance1 / 2
  #print "elapsed1 : %f" % elapsed1
  #print "Distance1 : %.1f" % distance1
  if(distance1 < THRESHOULD1):
    sensor1 =True
    time1 = time.time()
    #print "Sensor1 active"
    #print time1
  else:  
     lastactive1 = time.time()-time1
     #print "Last active %d",lastactive1
     if(time.time()-time1 > 2):
          sensor1 = False
          #print "Sensor1 deactive"      
           
  # ==============================================
   # Allow module to settle
  #time.sleep(0.5)

  # Set trigger to False (Low)
  GPIO.output(GPIO_TRIGGER2, False)

  # Allow module to settle
  time.sleep(0.01)

  # Send 10us pulse to trigger
  GPIO.output(GPIO_TRIGGER2, True)
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER2, False)
  start2 = time.time()

  while GPIO.input(GPIO_ECHO2)==0:
   start2 = time.time()

  while GPIO.input(GPIO_ECHO2)==1:
    stop2 = time.time()

  # Calculate pulse length
  elapsed2 = stop2-start2

  # Distance pulse travelled in that time is time
  # multiplied by the speed of sound (cm/s)
  distance2 = elapsed2 * 34300

  # That was the distance there and back so halve the value
  distance2 = distance2 / 2
  #print "elapsed2 : %f "% elapsed2
  #print "Distance2 : %.1f" % distance2
  #print "\n=====================\n"
  if(distance2 < THRESHOULD1):
    sensor2 =True
    time2 = time.time()
    #print "Sensor2 active"
    #print time2
  else : 
     if(time.time()-time2 > 2):
          sensor2 = False
          #print "Sensor2 deactive"

  #People detection logic
  if(sensor1 == False and sensor2 == False and time1 !=0 and time2 !=0):
    lastactive1 = time.time()-time1
    lastactive2 = time.time()-time2
    #print "last active 1 = %d lastactive2 =%d"%lastactive1,lastactive2
    if lastactive1<5 and lastactive2 < 5 :
        #print "Both sensors active"   
        if(time1>time2):
           people =people-1
        else:
           people = people +1
        time1 = 0
        time2 = 0
  
  if(people<0):
    people =0
  #print "people = %d "%people
  display.ShowInt(people)
 

#End of measurements
# Reset GPIO settings
GPIO.cleanup()
