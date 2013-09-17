#!/usr/bin/env python3
#
# Computer Networks
# Olin College
# Lab 1
# Alethea Butler <alethea@aletheabutler.com>
#

import transmitter


class Transmitter(transmitter.Transmitter):
    def __init__(self, channel, unit=1):
        transmitter.Transmitter.__init__(self, channel)
        self.unit = unit

    def send(self, string):
        self.put(encode(string))

    def encode(self, morse):
        if not morse.endswith(SK):
            morse += STRING_TO_MORSE[' '] + SK
        # Note that letter and word gaps are reduced by 1 unit do to the
        # trailing 1 unit gap on each character
        unit_encoding = {
            '.': ((self.unit, True), (self.unit, False)),
            '-': ((3 * self.unit, True), (self.unit, False)),
            ' ': ((2 * self.unit, False),),
            '_': ((6 * self.unit, False),)
        }
        atom = []
        for sym in morse:
            atom.extend(unit_encoding[sym])
        return atom


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

MORSE_TO_STRING = {morse: string for string, morse in STRING_TO_MORSE.items()}