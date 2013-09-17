#!/usr/bin/env python3
#
# Computer Networks
# Olin College
# Lab 1
# Alethea Butler <alethea@aletheabutler.com>
#

import atexit
import time
import RPi.GPIO as GPIO

atexit.register(GPIO.cleanup)
GPIO.setmode(GPIO.BOARD)

while True:
    GPIO.setup(15, GPIO.OUT)
    GPIO.output(15, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(15, GPIO.IN)
    start = time.time()
    while (GPIO.input(15) == GPIO.LOW):
        pass
    end = time.time()
    print(1e6 * (end - start))
