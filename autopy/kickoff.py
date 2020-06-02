import datetime
import time
import RPi.GPIO as GPIO
from Adafruit_LED_Backpack import SevenSegment

display = SevenSegment.SevenSegment(address=0x70, busnum=1)
display.begin()

faderState = True
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
faderPin = 24
GPIO.setup(faderPin, GPIO.OUT)
GPIO.output(faderPin, GPIO.HIGH)

def panelFader(state):
    if state == 'on':
        print("going high / on")
        GPIO.output(faderPin, GPIO.HIGH)
    if state == 'off':
        print("going low / off")
        GPIO.output(faderPin, GPIO.LOW)


while True:
    display.clear()
    stime = time.strftime("%I%M")
    itime = int(stime)
    display.print_float(itime, decimal_digits=0)
    display.set_colon(True)
    display.write_display()
    time.sleep(1.0)
    display.set_colon(False)
    display.write_display()
    time.sleep(1.0)
    curr_hour = time.localtime()[3]
    if (curr_hour >= 20 and faderState == True) or (curr_hour < 6 and faderState == True):
        faderState = False
        panelFader('off')
    elif curr_hour >= 6 and curr_hour < 20 and faderState == False:
        faderState = True
        panelFader('on')






