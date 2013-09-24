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


class Receiver:
    def __init__(self, pin, poll_freq):
        self.pin = pin
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
            duration, state = self.queue.get()
            decoded = self.decode(duration, state)
        return decoded

    def poll(self):
        message = None
        while message is None:
            try:
                duration, state = self.queue.get_nowait()
                message = self.decode(duration, state)
            except queue.Empty:
                return None
        return message

    def terminate(self):
        self.running = False
        self.worker.join()

    def read(self):
        self.pin.output(False)
        time.sleep(self.flush_delay)
        count = 0
        while not self.pin.input():
            count += 1
            time.sleep(self.edge_poll_freq)
        return count < self.threshold


class RawReceiver(Receiver):
    def __init__(self, channel, poll_freq=10):
        Receiver.__init__(self, channel, poll_freq)

    def decode(self, duration, state):
        return (duration, state)


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
            current = self.parent.read()
            if last != current:
                end = time.time()
                self.parent.queue.put((end - start, last))
                start = end
                last = current
