#!/usr/bin/python
import signal
import sys
import time
import RPi.GPIO as GPIO
from display import TM1637
import  pubsub
import getopt

if __name__ == '__main__': 
	# Usage
	usageInfo = """Usage:

	Use certificate based mutual authentication:
	python basicPubSub.py -e <endpoint> -r <rootCAFilePath> -c <certFilePath> -k <privateKeyFilePath>

	Use MQTT over WebSocket:
	python basicPubSub.py -e <endpoint> -r <rootCAFilePath> -w

	Type "python basicPubSub.py -h" for available options.
	"""
	# Help info
	helpInfo = """-e, --endpoint
		Your AWS IoT custom endpoint
	-r, --rootCA
		Root CA file path
	-c, --cert
		Certificate file path
	-k, --key
		Private key file path
	-w, --websocket
		Use MQTT over WebSocket
	-h, --help
		Help information


	"""

	# Read in command-line parameters
	useWebsocket = False
	host = ""
	rootCAPath = ""
	certificatePath = ""
	privateKeyPath = ""
	peoplecount = 0
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hwe:k:c:r:", ["help", "endpoint=", "key=","cert=","rootCA=", "websocket"])
		if len(opts) == 0:
			raise getopt.GetoptError("No input parameters!")
		for opt, arg in opts:
			if opt in ("-h", "--help"):
				print(helpInfo)
				exit(0)
			if opt in ("-e", "--endpoint"):
				host = arg
			if opt in ("-r", "--rootCA"):
				rootCAPath = arg
			if opt in ("-c", "--cert"):
				certificatePath = arg
			if opt in ("-k", "--key"):
				privateKeyPath = arg
			if opt in ("-w", "--websocket"):
				useWebsocket = True
	except getopt.GetoptError:
		print(usageInfo)
		exit(1)

	# Missing configuration notification
	missingConfiguration = False
	if not host:
		print("Missing '-e' or '--endpoint'")
		missingConfiguration = True
	if not rootCAPath:
		print("Missing '-r' or '--rootCA'")
		missingConfiguration = True
	if not useWebsocket:
		if not certificatePath:
			print("Missing '-c' or '--cert'")
			missingConfiguration = True
		if not privateKeyPath:
			print("Missing '-k' or '--key'")
			missingConfiguration = True
	if missingConfiguration:
		exit(2)


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


def interrupt_handler(signal, frame):
    GPIO.cleanup()
    sys.exit(0)

def getSensorStatus(GPIO_TRIGGER, GPIO_ECHO, time1):
  # Set trigger to False (Low)
  GPIO.output(GPIO_TRIGGER1, False)

  # Allow module to settle
  time.sleep(0.001)

  # Send 10us pulse to trigger
  GPIO.output(GPIO_TRIGGER, True)
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
  start1 = time.time()

  while GPIO.input(GPIO_ECHO) == 0:
    start1 = time.time()

  while GPIO.input(GPIO_ECHO) == 1:
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
     sensor1 = False
     lastactive1 = time.time()-time1
     #print "Last active %d",lastactive1
     if(time.time()-time1 > 2):
          sensor1 = False
          #print "Sensor1 deactive"      
  return sensor1, time1


signal.signal(signal.SIGINT, interrupt_handler)


#Variables for people count
time1 = 0
time2 = 0
people =0
#"""Confirm the display operation"""
display = TM1637(CLK=21, DIO=20, brightness=1.0)
display.Clear()

digits = [1, 2, 3, 4]
display.Show(digits)
time.sleep(3)

display.Clear()
PUBLISHING_TIME = 2
#Init complete
starttime=time.time()
people = 0



while True:
  if (time.time() - starttime) > (60.0 * PUBLISHING_TIME):
    starttime = time.time()
    pubsub.main(host, privateKeyPath,certificatePath, rootCAPath, useWebsocket, people)
    print "published to dynamodb"

  sensor1, time1 = getSensorStatus(GPIO_TRIGGER1, GPIO_ECHO1, time1)
  sensor2, time2 = getSensorStatus(GPIO_TRIGGER2, GPIO_ECHO2, time2)
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
 
# End of measurements
# Reset GPIO settings
GPIO.cleanup()
