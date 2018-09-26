from chunker import chunker
from utils import *
from progressbar import progress
from metadata import *

def encode(input_file: str, output_file: str)->None:
    file_size: int = getFileSize(input_file)
    x: int  = 0
    encode_str: bytes = metaDataGenerate() + b""
    for chunk in chunker(input_file):
        for data in chunk:
            encode_str += (data ^ 0xFF).to_bytes(1, 'little')
            x += 1
            progress(x, file_size, "Encode")
    print()
    storeFile(output_file, encode_str)
    return None

def decode(input_file: str, output_file: str)->None:
    file_size: int = getFileSize(input_file)
    x: int = 0
    decode_str: bytes =  b""
    if metaDataVerify(input_file):
        file_size: int = getFileSize(input_file)
        x: int = 0
        i: int = 0
        decode_str: bytes = b""
        for chunk in chunker(input_file):
            for data in chunk:
                if i > 64:
                    decode_str += (data ^ 0xFF).to_bytes(1, 'little')
                else:
                    i += 1
                x += 1
                progress(x, file_size, 'Decode')
        print()
        storeFile(output_file, decode_str)
    return None
