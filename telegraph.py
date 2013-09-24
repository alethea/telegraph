#!/usr/bin/env python3
#
# Computer Networks
# Olin College
# Lab 1
# Alethea Butler <alethea@aletheabutler.com>
#

import queue
import threading
import transmitter
import receiver
from morse import encode, decode, TX_SK, RX_SK


class Transmitter(transmitter.Transmitter):
    def __init__(self, pin, freq=1):
        self.freq = freq
        transmitter.Transmitter.__init__(self, pin)

    def send(self, string):
        self.queue.put(encode(string))

    def encode(self, morse):
        if not morse.endswith(TX_SK):
            morse += TX_SK
        unit = 1 / self.freq
        # Note that letter and word gaps are reduced by 1 unit do to the
        # trailing 1 unit gap on each character
        unit_encoding = {
            '.': ((unit, True), (unit, False)),
            '-': ((3 * unit, True), (unit, False)),
            ' ': ((2 * unit, False),),
            '_': ((6 * unit, False),)
        }
        for sym in morse:
            for pulse in unit_encoding[sym]:
                yield pulse


class Receiver(receiver.Receiver):
    def __init__(self, pin, freq=1):
        self.freq = freq
        self.message = []
        receiver.Receiver.__init__(self, pin, 15)

    def decode(self, duration, state):
        unit = 1 / self.freq
        if state:
            if duration < 2 * unit:
                self.message.append('.')
            else:
                self.message.append('-')
        else:
            if duration < 2 * unit:
                pass
            elif duration < 5 * unit:
                self.message.append(' ')
            else:
                self.message.append('_')
        if self.message[-len(RX_SK):] == RX_SK:
            decoded = decode(''.join(self.message)).strip()
            self.message = []
            return decoded
        return None


class Relay:
    def __init__(self, rx, tx, address):
        self.rx = rx
        self.tx = tx
        self.address = address
        self.queue = queue.Queue()
        self.running = True
        self.router = Router(self)
        self.router.start()

    def send(self, address, message):
        self.tx.send(' '.join((address, message)))

    def poll(self):
        try:
            return self.queue.get_nowait()
        except queue.Empty:
            return None

    def listen(self):
        return self.queue.get()


class Router(threading.Thread):
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.daemon = True
        self.parent = parent

    def run(self):
        while self.parent.running:
            message = self.parent.rx.listen()
            address = self.parent.address.upper() + ' '
            if message.startswith(address):
                self.parent.queue.put(message[len(address):])
            else:
                self.parent.tx.send(message)
