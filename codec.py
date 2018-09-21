#!/usr/bin/python3
import argparse
from sys import exit

from encoders_decoders import inverter as inv
from encoders_decoders import xor
from encoders_decoders import xor_inv

def cmd_line():
    """Commande line supported by codec.py"""
    parser = argparse.ArgumentParser(description="Encode decode any file"
        ,prog='codec') #usage='codec -e'
    parser.add_argument('-e','--encoder', help='Encoder number', type=int)
    parser.add_argument('-d', '--decoder', help='Decoder numer', type=int)
    parser.add_argument('-i', '--input', help='Input file name to encode/decode'
        , type=str)
    parser.add_argument('-o', '--output', help='Output file name', type=str)
    parser.add_argument('-l', '--list', help='list of all encode/decoder'
        ,action='store_true')
    return parser.parse_args()


class EncoderDecoder:
    """docstring for EncoderDecoder"""
    def __init__(self, label: int, enc_func, dec_func, description: str):
        self.label = label
        self.enc_func = enc_func
        self.dec_func = dec_func
        self.description = description

def build_enc_dec()->dict:
    enc_dec_info: dict = {
    1: EncoderDecoder(1, inv.encode, inv.decode, "Inv Encoder/Decoder"),
    2: EncoderDecoder(2, xor.encode, xor.decode, 'Xor classic Encoder/Decoder'),
    3: EncoderDecoder(3, xor_inv.encode, xor_inv.decode, 'Xor & Inv Encoder/Decoder')
    }
    return enc_dec_info

def build_list():
    for (i, encoder) in build_enc_dec().items():
        print("\033[1;34m{}: {}\033[0m".format(encoder.label, 
            encoder.description))

def main():
    args = cmd_line()
    if args.input and args.output:
        enc_dec = build_enc_dec()
        if args.encoder:
            enc_dec[args.encoder].enc_func(args.input, args.output)
        elif args.decoder:
            enc_dec[args.decoder].dec_func(args.input, args.output)
    if args.list:
        build_list()
        exit(0)

if __name__ == '__main__':
    main()
