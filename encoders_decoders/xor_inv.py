from chunker import chunker
from metadata import *
from os import stat
import numpy as np


WORD_SIZE: int = 8

def encode(input_file: str, output_file: str, validity: int = 0, bar: bool = False)->None:
    status: bool = True
    file_size: int = stat(input_file).st_size
    middle: int = int((file_size // WORD_SIZE) / 2)* WORD_SIZE
    with open(output_file, 'wb') as destination_file:
        if validity == 0:
            destination_file.write(metaDataGenerate())
        else:
            destination_file.write(metaDataGenerate(validity))
        with open(input_file, 'rb') as source_file:
            destination_file.write(np.bitwise_xor(
                np.frombuffer(
                    source_file.read(middle), dtype=np.uint64),
                0x6565656565656565).tobytes())
            source_file.seek(middle)
            destination_file.write(
                np.invert(np.fromfile(
                    source_file, dtype=np.uint64)).tobytes())
        residu: int = 0
        residu = file_size % WORD_SIZE
        if residu != 0:
            for data in chunker(input_file, residu):
                if status:
                    destination_file.write((data ^ 0x65).to_bytes(1, 'little'))
                else:
                    destination_file.write(
                        (data ^ 0xFF).to_bytes(1, 'little'))
                status = not status
    return None


def decode(input_file: str, output_file: str, bar: bool = False)->None:
    if metaDataVerify(input_file):
        status: bool = True
        file_size: int = stat(input_file).st_size
        middle: int = int(((file_size - 64) // WORD_SIZE) / 2) * WORD_SIZE
        with open(output_file, 'wb') as destination_file:
            with open(input_file, 'rb') as source_file:
                source_file.seek(64)
                destination_file.write(np.bitwise_xor(
                    np.frombuffer(
                        source_file.read(middle), dtype=np.uint64),
                    0x6565656565656565).tobytes())
                source_file.seek(middle + 64)
                destination_file.write(
                    np.invert(np.fromfile(
                        source_file, dtype=np.uint64)).tobytes())
            residu: int = 0
            residu = (file_size - 64) % WORD_SIZE
            if residu != 0:
                for data in chunker(input_file, residu):
                    if status:
                        destination_file.write(
                            (data ^ 0x65).to_bytes(1, 'little'))
                    else:
                        destination_file.write(
                            (data ^ 0xFF).to_bytes(1, 'little'))
                    status = not status

    return None
