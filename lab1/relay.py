#!/usr/bin/env python3
#
# Computer Networks
# Olin College
# Lab 1
# Alethea Butler <alethea@aletheabutler.com>
#

import queue
import threading


class Relay:
    def __init__(self, rx, tx, address):
        self.rx = rx
        self.tx = tx
        self.queue = queue.Queue()
        self.address = address.upper() + ' '
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
            if message.startswith(self.parent.address):
                self.parent.queue.put(message[len(self.parent.address):])
            else:
                self.parent.tx.send(message)
