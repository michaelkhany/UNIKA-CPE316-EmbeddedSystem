# Import libraries
import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode #
GPIO.setmode(GPIO.BCM)

# pin locations
GPIO.setup(17,GPIO.OUT) # servo motor
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_UP) # touch sensor

# pin and the hertz
servo1 = GPIO.PWM(17, 50)

servo1.start(0)

try:
    k = 0 # not yet at 90 degrees
    while True:
        if GPIO.input(21) == True:
            print('Touch Detected')
        time.sleep(0.5)
        i = 1
        j = 5 # step count
        if k == 1:
            servo1.ChangeDutyCycle(2) # to 0 degrees
            time.sleep(0.5)
            servo1.ChangeDutyCycle(0)
            k = 0
        else:
            while i<j+1:
                servo1.ChangeDutyCycle(2+((90/18)*i/j)) # to 90 degrees
                time.sleep(0.3)
                servo1.ChangeDutyCycle(0)
                i = i + 1
                if i == 6:
                    k = k + 1 # 90 degree completed, prepare for the 0 degree turn
                    if GPIO.input(21) == False:
                        print('No Touch Detected')
                        time.sleep(0.5)
finally: #Clean things up at the end
    servo1.stop()
    GPIO.cleanup()
    print("Goodbye!")