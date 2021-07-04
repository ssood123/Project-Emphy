

import RPi.GPIO as GPIO
import time

# BCM I/O pins and pin numbers

GPIO.setmode(GPIO.BCM)
pbswitch_pin = 4
example_pin = 18  # will be replaced with start/stop and voice button pins



GPIO.setup(pbswitch_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(example_pin, GPIO.OUT)

# Define and set (initialize) the  output state as False

example_state = False


# pbswitch event monitoring loop: Button pressed keeps the loop active and once release/ pressed in our case it stops

while True:
    new_input_event = GPIO.input(pbswitch_pin)
    if new_input_event == False: 
        example_state = not example_state
        GPIO.output(example_pin, GPIO.HIGH)
    time.sleep(.1)
        GPIO.output(example_pin, GPIO.LOW)
    time.sleep(.1)