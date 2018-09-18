#!/usr/bin/python3
import argparse

def cmd_line():
    parser = argparse.ArgumentParser(description="Encode decode any file"
        ,prog='codec') #usage='codec -e'
    parser.add_argument('-e','--encoder', help='Encoder number', type=int)
    parser.add_argument('-d', '--decoder', help='Decoder numer', type=int)
    parser.add_argument('-f', '--file', help='Path of file to encode/decode'
        , type=str)
    parser.add_argument('-l', '-list', help='list of all encode/decoder'
        ,action='store_true')
    return parser.parse_args()


def main():
    args = cmd_line()


if __name__ == '__main__':
    main()
