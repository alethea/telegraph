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
from relay import Relay

def main():
    atexit.register(GPIO.cleanup)

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)

    tx = Transmitter(26)
    rx = Receiver(15)

    address = input('Address: ')

    relay = Relay(rx, tx, address)

    print ('Morse relay ready')
    while True:
        try:
            address = input('To: ')
            if len(address) > 0:
                body = input('Message: ')
                if len(body) > 0:
                    relay.send(address, body)
                else:
                    print('Empty message not sent')
        except(EOFError):
            print('\nSending unsent messages')
            tx.join()
            break
        message = relay.poll()
        if message is None:
            print('No new messages')
        while message is not None:
            print('Received: ' + message)
            message = relay.poll()


if __name__ == '__main__':
    main()
