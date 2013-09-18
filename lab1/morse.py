#!/usr/bin/env python3
#
# Computer Networks
# Olin College
# Lab 1
# Alethea Butler <alethea@aletheabutler.com>
#

import transmitter
import receiver


class Transmitter(transmitter.Transmitter):
    def __init__(self, channel, freq=1):
        self.freq = freq
        transmitter.Transmitter.__init__(self, channel)

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
        message = []
        for sym in morse:
            message.extend(unit_encoding[sym])
        return message

class Receiver(receiver.Receiver):
    def __init__(self, channel, freq=1):
        self.freq = freq
        self.message = []
        receiver.Receiver.__init__(self, channel, 15)

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
            return decode(''.join(self.message)).strip()
        return None


def encode(string):
    morse_list = [STRING_TO_MORSE[char] for char in string.upper()]
    return ' '.join(morse_list).replace(' _ ', '_')


def decode(morse):
    morse_words = morse.split('_')
    string_words = []
    for word in morse_words:
        if word == SK:
            break
        string_words.append(''.join([MORSE_TO_STRING[sym] for sym in word.split(' ')]))
    return ' '.join(string_words)


STRING_TO_MORSE = {
    '': '',
    ' ': '_',
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    '0': '-----'
}

SK = '...-.-'
RX_SK = list(SK)
TX_SK = '_' + SK + '_'

MORSE_TO_STRING = {morse: string for string, morse in STRING_TO_MORSE.items()}
