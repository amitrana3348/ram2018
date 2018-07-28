#!/usr/bin/env python

import RPi.GPIO as GPIO
import time, sys
from Adafruit_IO import Client





from firebase import firebase
fb = firebase.FirebaseApplication('https://ramkarde-3348.firebaseio.com/', None)

aio = Client('Ramkarde', '5f5fc6b5d6ec40f5a1f3ad6406342c83')

#############BELOW FOR FLOW SENSOR ##################3
FLOW_SENSOR = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

global count
count = 0

def countPulse(channel):
   global count
   count = count+1
   #print count
############################ FLOW SENSOR END ##################################


#############BELOW FOR BMP SENSOR ##################
import Adafruit_BMP.BMP085 as BMP085
from time import sleep
sensor = BMP085.BMP085()

################# END #################################

#############BELOW FOR DS18B20 SENSOR ##################
import glob
import os
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f
################# END #################################

#############BELOW FOR All IO ##################
GPIO.setmode(GPIO.BCM)
relay1 = 24
relay2 = 25
relay3 = 8
relay4 = 7
buzzer = 23
gas = 26
cds = 20
dr = 21
flow = 6
fire = 5
GPIO.setup(relay1,GPIO.OUT)
GPIO.setup(relay2,GPIO.OUT)
GPIO.setup(relay3,GPIO.OUT)
GPIO.setup(relay4,GPIO.OUT)
GPIO.setup(buzzer,GPIO.OUT)

GPIO.setup(cds,GPIO.OUT)
GPIO.output(cds,True)
GPIO.setup(dr,GPIO.IN)
GPIO.setup(fire,GPIO.IN)
GPIO.setup(gas,GPIO.IN)
################# END #################################

#############BELOW FOR BH1750 SENSOR ##################
import smbus
import time

# Define some constants from the datasheet

DEVICE     = 0x23 # Default device I2C address

POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number. Optional parameter 'decimals'
  # will round to specified number of decimal places.
  result=(data[1] + (256 * data[0])) / 1.2
  return (result)

def readLight(addr=DEVICE):
  # Read data from I2C interface
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)
################# END #################################


while True:
   print 'Lux level is '
   lightLevel=readLight()
   lightLevel = round(lightLevel,2)
   print lightLevel
   fb.put('ram',"lux",lightLevel) #"path","property_Name",
   aio.send('lux',lightLevel) ########### 1
   print '\n\n'
   GPIO.add_event_detect(FLOW_SENSOR, GPIO.RISING, callback=countPulse)
   time.sleep(1)
   GPIO.remove_event_detect(FLOW_SENSOR)
   print count
   flow = count / 7.5
   flow = round(flow,2)
   aio.send('flow',flow)      ########### 2
   print "flow rate = {0} Liter/min".format(flow)
   fb.put('ram',"flow",flow) #"path","property_Name",property_Value
   ######################################################################33
   if GPIO.input(dr) == True:
      print "Motion detected"
      aio.send('motion','1')     ########### 3
      fb.put('ram',"motion",'0') #"path","property_Name",property_Value
   else:
      aio.send('motion','0')
      fb.put('ram',"motion",'1')

   if GPIO.input(fire) == False:
      print "Fire detected"
      aio.send('fire','1')       ########### 4
      fb.put('ram',"fire",'1')
   else:
      aio.send('fire','0')
      fb.put('ram',"fire",'0')

   if GPIO.input(gas) == False:
      print "Gas detected"
      #aio.send('gas','1')     ########### 5
      fb.put('ram',"gas",'1')
   else:
      #aio.send('gas','0')
      fb.put('ram',"gas",'0')
      
#######################################################################
   temperature = sensor.read_temperature()
   aio.send('temp',temperature)
   fb.put('ram',"temp",temperature)
   pressure = sensor.read_pressure()
   aio.send('pressure',pressure) ########### 6
   fb.put('ram',"pressure",pressure)
   altitude = sensor.read_altitude()
   print temperature
   print pressure
   print altitude
   #######################################################################
   data = aio.receive('relay1')
   print 'relay1 =' + data.value
   if data.value == 'ON':
      GPIO.output(relay1,True)
   if data.value == 'OFF':
      GPIO.output(relay1,False)
      
   data = aio.receive('relay2')
   print 'relay2 =' + data.value
   if data.value == 'ON':
      GPIO.output(relay2,True)
   if data.value == 'OFF':
      GPIO.output(relay2,False)

   data = aio.receive('relay3')
   print 'relay3 =' + data.value
   if data.value == 'ON':
      GPIO.output(relay3,True)
   if data.value == 'OFF':
     GPIO.output(relay3,False)

   data = aio.receive('relay4')
   print 'relay4 =' + data.value
   if data.value == 'ON':
      GPIO.output(relay4,True)
   if data.value == 'OFF':
     GPIO.output(relay4,False)
      
   sleep(4)
