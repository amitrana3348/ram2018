import RPi.GPIO as GPIO
from time import sleep
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
while True:
    if GPIO.input(dr) == True:
        print "Motion detected"
    if GPIO.input(fire) == False:
        print "Fire detected"
    if GPIO.input(gas) == False:
        print "Gas detected"
    GPIO.output(buzzer,True)
    GPIO.output(relay1,True)
    GPIO.output(relay2,True)
    GPIO.output(relay3,True)
    GPIO.output(relay4,True)
    sleep(2)
    GPIO.output(buzzer,False)
    GPIO.output(relay1,False)
    GPIO.output(relay2,False)
    GPIO.output(relay3,False)
    GPIO.output(relay4,False)
    sleep(2)


