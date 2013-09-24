#!/usr/bin/env python3
#
# Computer Networks
# Olin College
# Lab 1
# Alethea Butler <alethea@aletheabutler.com>
#

import time
import threading
import queue


class Transmitter:
    def __init__(self, pin):
        self.pin = pin
        self.queue = queue.Queue()
        self.running = True
        self.worker = TransmitterWorker(self)
        self.worker.start()

    def send(self, atom):
        self.queue.put(atom)

    def join(self):
        self.queue.join()

    def terminate(self):
        self.running = False
        self.worker.join()



class TransmitterWorker(threading.Thread):
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.daemon = True
        self.parent = parent

    def run(self):
        while self.parent.running:
            try:
                atom = self.parent.queue.get_nowait()
            except queue.Empty:
                self.parent.pin.output(False)
                atom = self.parent.queue.get()
            for duration, state in self.parent.encode(atom):
                self.parent.pin.output(state)
                time.sleep(duration)
            self.parent.queue.task_done()
