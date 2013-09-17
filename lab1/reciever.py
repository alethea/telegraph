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


poll_freq = 1e-5
flush_delay = 0.01
def read(channel):
    GPIO.setup(channel, GPIO.OUT)
    GPIO.output(channel, GPIO.LOW)
    time.sleep(flush_delay)
    GPIO.setup(channel, GPIO.IN)
    count = 0
    while (GPIO.input(channel) == GPIO.LOW):
        count += 1
        time.sleep(poll_freq)
    return count

while True:
    print(read(15))
