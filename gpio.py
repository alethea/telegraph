#!/usr/bin/env python3
#
# Computer Networks
# Olin College
# Lab 1
# Alethea Butler <alethea@aletheabutler.com>
#

import RPi.GPIO


class GPIO:
    def __init__(self, gpio=RPi.GPIO):
        self.gpio = gpio
        self.gpio.setmode(self.gpio.BOARD)

    def pin(self, channel):
        return Pin(self.gpio, channel)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.gpio.cleanup()
        return False


class Pin:
    def __init__(self, gpio, channel):
        self.gpio = gpio
        self.channel = channel
        self.mode = self.gpio.IN
        self.gpio.setup(self.channel, self.gpio.IN)

    def output(self, state):
        if self.mode != self.gpio.OUT:
            self.mode = self.gpio.OUT
            self.gpio.setup(self.channel, self.gpio.OUT)
        if state:
            self.gpio.output(self.channel, self.gpio.HIGH)
        else:
            self.gpio.output(self.channel, self.gpio.LOW)

    def input(self):
        if self.mode != self.gpio.IN:
            self.mode = self.gpio.IN
            self.gpio.setup(self.channel, self.gpio.IN)
        return self.gpio.input(self.channel) == self.gpio.HIGH
