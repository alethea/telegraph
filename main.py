#!/usr/bin/env python3
#
# Computer Networks
# Olin College
# Lab 1
# Alethea Butler <alethea@aletheabutler.com>
#

from morse import MorseEncodingError
from telegraph import Transmitter, Receiver, Relay
from gpio import GPIO


def main():
    with GPIO() as gpio:
        tx = Transmitter(gpio.pin(26))
        rx = Receiver(gpio.pin(15))
        relay = Relay(rx, tx, input('Address: '))

        print('Morse relay ready')
        while True:
            try:
                address = input('To: ')
                if len(address) > 0:
                    body = input('Message: ')
                    if len(body) > 0:
                        try:
                            relay.send(address, body)
                        except MorseEncodingError:
                            print('Could not convert to Morse code')
                    else:
                        print('Empty message not sent')
            except(EOFError):
                print('\nSending unsent messages')
                rx.terminate()
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
