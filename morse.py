#!/usr/bin/env python3
#
# Computer Networks
# Olin College
# Lab 1
# Alethea Butler <alethea@aletheabutler.com>
#


def encode(string):
    try:
        morse_list = [STRING_TO_MORSE[char] for char in string.upper()]
    except KeyError as error:
        raise MorseEncodingError from error
    return ' '.join(morse_list).replace(' _ ', '_')


def decode(morse):
    symbols = morse.replace('_', ' _ ')
    chars = []
    try:
        for sym in symbols.split():
            if sym == SK:
                break
            chars.append(MORSE_TO_STRING[sym])
    except KeyError as error:
        raise MorseEncodingError from error
    return ''.join(chars)


class MorseEncodingError(Exception):
    pass


STRING_TO_MORSE = {
    ' ': ' ',
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
    '0': '-----',
    '.': '.-.-.-',
    ',': '--..--',
    '?': '..--..',
    '\'': '.----.',
    '!': '-.-.--',
    '/': '-..-.',
    '(': '-.--.',
    ')': '-.--.-',
    '&': '.-...',
    ':': '---...',
    ';': '-.-.-.',
    '=': '-...-',
    '+': '.-.-.',
    '-': '-....-',
    '_': '..--.-',
    '"': '.-..-.',
    '$': '...-..-',
    '@': '.--.-.'
}

SK = '...-.-'
RX_SK = list(SK)
TX_SK = '_' + SK + '_'

MORSE_TO_STRING = {morse: string for string, morse in STRING_TO_MORSE.items()}
