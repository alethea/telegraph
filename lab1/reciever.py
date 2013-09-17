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

poll_freq = 5e-5
flush_delay = 0.01
while True:
    GPIO.setup(15, GPIO.OUT)
    GPIO.output(15, GPIO.LOW)
    time.sleep(flush_delay)
    GPIO.setup(15, GPIO.IN)
    count = 0
    while (GPIO.input(15) == GPIO.LOW):
        count += 1
        time.sleep(poll_freq)
    print(count)
