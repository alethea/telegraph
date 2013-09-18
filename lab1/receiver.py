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


class Receiver:
    def __init__(self, channel, poll_freq):
        self.channel = channel
        self.poll_freq = poll_freq
        self.queue = queue.Queue()
        self.worker = ReceiverWorker(self)
        self.running = True
        self.worker.start()

    edge_poll_freq = 1e-5
    flush_delay = 0.01
    threshold = 2

    def listen(self):
        decoded = None
        while decoded is None:
            decoded = self.decode(self.queue.get())
        return decoded

    def terminate(self):
        self.running = False
        self.worker.join()

    def _read(self):
        GPIO.setup(self.channel, GPIO.OUT)
        GPIO.output(self.channel, GPIO.LOW)
        time.sleep(self.flush_delay)
        GPIO.setup(self.channel, GPIO.IN)
        count = 0
        while (GPIO.input(self.channel) == GPIO.LOW):
            count += 1
            time.sleep(self.edge_poll_freq)
        return count < self.threshold


class RawReceiver(Receiver):
    def __init__(self, channel, poll_freq=10):
        Receiver.__init__(self, channel, poll_freq)

    def decode(self, atom):
        return atom


class ReceiverWorker(threading.Thread):
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.daemon = True
        self.parent = parent

    def run(self):
        last = False
        start = time.time()
        while self.parent.running:
            time.sleep(1 / self.parent.poll_freq)
            current = self.parent._read()
            if last != current:
                end = time.time()
                self.parent.queue.put((end - start, last))
                start = end
                last = current
