#!/usr/bin/env python3
#
# Computer Networks
# Olin College
# Lab 1
# Alethea Butler <alethea@aletheabutler.com>
#

import atexit
import RPi.GPIO as GPIO
from morse import Transmitter

def main():
    atexit.register(GPIO.cleanup)

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)

    tx = Transmitter(26, 0.25)

    print ('Morse transmitter ready')
    while True:
        try:
            string = input('> ')
            if len(string) > 0:
                tx.send(string)
        except(EOFError):
            print('\nSending unsent messages')
            tx.join()
            break


if __name__ == '__main__':
    main()
