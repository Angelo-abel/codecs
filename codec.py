#!/usr/bin/python3
import argparse
from chunker import chunker


def cmd_line():
    """Commande line supported by codec.py"""
    parser = argparse.ArgumentParser(description="Encode decode any file"
        ,prog='codec') #usage='codec -e'
    parser.add_argument('-e','--encoder', help='Encoder number', type=int)
    parser.add_argument('-d', '--decoder', help='Decoder numer', type=int)
    parser.add_argument('-f', '--file', help='Path of file to encode/decode'
        , type=str)
    parser.add_argument('-l', '-list', help='list of all encode/decoder'
        ,action='store_true')
    return parser.parse_args()


class EncoderDecoder:
    """docstring for EncoderDecoder"""
    def __init__(self, label: int, enc_func, dec_func, description: str):
        self.label = label
        self.enc_func = enc_func
        self.dec_func = dec_func
        self.description = description


def main():
    args = cmd_line()


if __name__ == '__main__':
    main()
