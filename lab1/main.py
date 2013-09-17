#!/usr/bin/env python3
#
# Computer Networks
# Olin College
# Lab 1
# Alethea Butler <alethea@aletheabutler.com>
# 2013-09-16
#

import atexit
import time
import RPi.GPIO as GPIO
from transmitter import Transmitter

atexit.register(GPIO.cleanup)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)

tx = Transmitter(26)
time.sleep(1)
tx.on(0.5)
tx.off(0.5)
tx.on(0.5)
tx.join()
