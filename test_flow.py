#!/usr/bin/env python

import RPi.GPIO as GPIO
import time, sys

FLOW_SENSOR = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

global count
count = 0

def countPulse(channel):
   global count
   count = count+1
   #print count



while True:
    GPIO.add_event_detect(FLOW_SENSOR, GPIO.RISING, callback=countPulse)
    time.sleep(1)
    GPIO.remove_event_detect(FLOW_SENSOR)
    print count
    flow = count / 7.5
    flow = round(flow,2)
    print "flow rate = {0} Liter/min".format(flow)
