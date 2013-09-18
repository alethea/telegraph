#!/usr/bin/env python3
#
# Computer Networks
# Olin College
# Lab 1
# Alethea Butler <alethea@aletheabutler.com>
#

import atexit
import RPi.GPIO as GPIO
from morse import Transmitter, Receiver

def main():
    atexit.register(GPIO.cleanup)

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)

    tx = Transmitter(26)
    rx = Receiver(15)

    print ('Morse transceiver ready')
    while True:
        try:
            message = rx.poll()
            if message is not None:
                print('< ' + message)
            string = input('> ')
            if len(string) > 0:
                tx.send(string)
        except(EOFError):
            print('\nSending unsent messages')
            rx.terminate()
            tx.join()
            break


if __name__ == '__main__':
    main()
