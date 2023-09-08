import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def print_msg(x):
    print("Button {} was pushed!".format(x))


while True:
    input_01 = GPIO.input(16)
    input_02 = GPIO.input(20)
    input_03 = GPIO.input(21)

    if input_01 == False:
        print_msg(1)
        time.sleep(0.2)
    
    if input_02 == False:
        print_msg(2)
        time.sleep(0.2)
        
    if input_03 == False:
        print_msg(3)
        time.sleep(0.2)
        
    
