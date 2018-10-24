from chunker import chunker
from os import stat
from metadata import *
import numpy as np


WORD_SIZE: int = 8

def encode(input_file: str, output_file: str, validity: int = 0, bar: bool = False)->None:
    with open(output_file, 'wb') as destination_file:
        if validity == 0:
            destination_file.write(metaDataGenerate())
        else:
            destination_file.write(metaDataGenerate(validity))
        destination_file.write(np.invert(
            np.fromfile(input_file, dtype=np.uint64)).tobytes())
        residu: int = 0
        residu = stat(input_file).st_size % WORD_SIZE
        if residu != 0:
            for data in chunker(input_file, residu):
                destination_file.write((data ^ 0xFF).to_bytes(1, 'little'))
    return None


def decode(input_file: str, output_file: str, bar: bool = False)->None:
    if metaDataVerify(input_file):
        with open(output_file, 'wb') as destination_file:
            with open(input_file, 'rb') as source_file:
                source_file.seek(64)
                destination_file.write(np.invert(
                    np.fromfile(source_file, dtype=np.uint64)).tobytes())
            residu: int = 0
            residu = (stat(input_file).st_size - 64) % WORD_SIZE
            if residu != 0:
                for data in chunker(input_file, residu):
                    destination_file.write((data ^ 0xFF).to_bytes(1, 'little'))
        return None
