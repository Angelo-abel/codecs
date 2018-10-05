#!/usr/bin/python3
import argparse
import sys
from datetime import datetime
from hashlib import blake2b

from encoders_decoders import inverter as inv
from encoders_decoders import xor
from encoders_decoders import xor_inv
from encoders_decoders import xor_pass_phrase
from UserException import NotEncodedError, PassPhraseError


def displayError(error: str):
    RED: str = "\33[1;31m"
    NEUTRAL: str = "\33[1;0m"
    print("{}{}{}".format(RED, error, NEUTRAL))

def cmdLine():
    """Commande line supported by codec.py"""
    parser = argparse.ArgumentParser(description="Encode decode any file"
        ,prog='codec') #usage='codec -e'
    parser.add_argument('-e','--encoder', help='Encoder number', type=int)
    parser.add_argument('-d', '--decoder', help='Decoder numer', type=int)
    parser.add_argument('-i', '--input', help='Input file name to encode/decode', type=str)
    parser.add_argument('-o', '--output', help='Output file name', type=str)
    parser.add_argument('-l', '--list', help='list of all encode/decoder'
        ,action='store_true')
    parser.add_argument('-p', '--passphrase', help='Pass phrase to encode file', type=str)
    return parser.parse_args()


class EncoderDecoder:
    """docstring for EncoderDecoder"""
    def __init__(self, label: int, enc_func, dec_func, description: str):
        self.label = label
        self.enc_func = enc_func
        self.dec_func = dec_func
        self.description = description

def buildEncDec()->dict:
    enc_dec_info: dict = {
    1: EncoderDecoder(1, inv.encode, inv.decode, "Inv Encoder/Decoder"),
    2: EncoderDecoder(2, xor.encode, xor.decode, 'Xor classic Encoder/Decoder'),
    3: EncoderDecoder(3, xor_inv.encode, xor_inv.decode, 'Xor & Inv Encoder/Decoder'),
    4: EncoderDecoder(4, xor_pass_phrase.encode, xor_pass_phrase.decode, 'Xor with pass phrase')
    }
    return enc_dec_info

def buildList():
    for (i, encoder) in buildEncDec().items():
        print("\033[1;34m{}: {}\033[0m".format(encoder.label, 
            encoder.description))

def passPhraseEncode(pass_phrase: str)->bytes:
    return blake2b(pass_phrase.encode('utf8')).hexdigest().encode('utf8')


if __name__ == '__main__':
    start_time = datetime.now()
    args = cmdLine()
    try:
        if args.input and args.output:   
            enc_dec = buildEncDec()
            if args.encoder:
                if args.encoder in (4, 0):
                    if args.passphrase:
                        enc_dec[args.encoder].enc_func(args.input, args.output, passPhraseEncode(args.passphrase))
                    else:
                        raise PassPhraseError
                else:
                    enc_dec[args.encoder].enc_func(args.input, args.output)
            elif args.decoder:
                if args.decoder in (4, 0):
                    if args.passphrase:
                        enc_dec[args.decoder].dec_func(args.input, args.output, passPhraseEncode(args.passphrase))
                    else:
                        raise PassPhraseError
                else:
                    enc_dec[args.decoder].dec_func(args.input, args.output)
            displayError(datetime.now()-start_time)
            sys.exit(0)
        if args.list:
            buildList()
            sys.exit(0)

    except FileNotFoundError:
        displayError("The file doesn't found")
        sys.exit(-1)
    except FileExistsError:
        displayError("The file doesn't exists")
        sys.exit(-1)
    except PermissionError:
        displayError("Permission denied to write output file in this location {}".format(args.output))
        exit(-1)
    except NotEncodedError:
        displayError("This file is not encoded")
        exit(-1)
    except PassPhraseError:
        displayError("Please enter pass phrase")
        exit(-1)
    #except Exception as exception:
    #    displayError("Something went wrong. Operation will abort!!")
    #    sys.exit(-1)
