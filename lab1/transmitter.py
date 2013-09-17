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
        self.worker = TransmitterWorker(self)
        self.worker.start()

    def on(self, duration):
        self.queue.put((duration, GPIO.HIGH))

    def off(self, duration):
        self.queue.put((duration, GPIO.LOW))

    def join(self):
        self.queue.join()


class TransmitterWorker(threading.Thread):
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.daemon = True
        self.parent = parent

    def run(self):
        while True:
            try:
                duration, state = self.parent.queue.get_nowait()
            except queue.Empty:
                GPIO.output(self.parent.channel, GPIO.LOW)
                duration, state = self.parent.queue.get()
            GPIO.output(self.parent.channel, state)
            time.sleep(duration)
            self.parent.queue.task_done()
