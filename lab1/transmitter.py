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
import RPi.GPIO as GPIO


class Transmitter:
    def __init__(self, channel):
        GPIO.setup(channel, GPIO.OUT, initial=GPIO.LOW)
        self.channel = channel
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


class RawTransmitter(Transmitter):
    def encode(self, atom):
        return [atom]

    def on(self, duration):
        self.send((duration, GPIO.HIGH))

    def off(self, duration):
        self.send((duration, GPIO.LOW))


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
                GPIO.output(self.parent.channel, GPIO.LOW)
                atom = self.parent.queue.get()
            for duration, state in self.parent.encode(atom):
                GPIO.output(self.parent.channel, state)
                time.sleep(duration)
            self.parent.queue.task_done()
