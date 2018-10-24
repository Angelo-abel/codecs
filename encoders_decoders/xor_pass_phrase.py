from chunker import chunker
from metadata import *
from os import stat
import numpy as np


WORD_SIZE: int = 8

def encode(input_file: str, output_file: str, pass_phrase: bytes,
    validity: int = 0, bar: bool = False)->None:
    file_size: int = stat(input_file).st_size
    quart = int((file_size // WORD_SIZE) / 16) * WORD_SIZE
    with open(output_file, 'wb') as destination_file:
        if validity == 0:
            destination_file.write(metaDataGenerate())
        else:
            destination_file.write(metaDataGenerate(validity))
        np_pass_phrase = np.frombuffer(pass_phrase, dtype=np.uint64)
        with open(input_file, 'rb') as source_file:
            i: int = 0
            last_quart: int = 0
            for data in np_pass_phrase:
                source_file.seek(quart*i)
                destination_file.write(
                    np.bitwise_xor(np.frombuffer(
                        source_file.read(
                            quart), dtype=np.uint64), data).tobytes())
                i += 1
                last_index = quart * i
            residu: int = 0
            residu = file_size % WORD_SIZE
            source_file.seek(last_index)
            destination_file.write(
                np.bitwise_xor(np.frombuffer(source_file.read(
                    file_size - (
                        last_index + residu)
                    ), dtype=np.uint64), np_pass_phrase[0]).tobytes())
            if residu != 0:
                i = 0
                for data in chunker(input_file, residu):
                    destination_file.write(
                        (data ^ pass_phrase[i]).to_bytes(1, 'little'))
                    i += 1
    return None


def decode(input_file: str, output_file: str, pass_phrase: bytes, bar: bool = False)->None:
    if metaDataVerify(input_file):
        file_size: int = stat(input_file).st_size - 64
        quart: int = int(((file_size) // WORD_SIZE) / 16) * WORD_SIZE
        np_pass_phrase = np.frombuffer(pass_phrase, dtype=np.uint64)
        with open(output_file, 'wb') as destination_file:
            with open(input_file, 'rb') as source_file:
                i: int = 0
                last_index: int = 0
                for data in np_pass_phrase:
                    source_file.seek(64 + (quart * i))
                    destination_file.write(
                        np.bitwise_xor(np.frombuffer(
                            source_file.read(
                                quart), dtype=np.uint64), data).tobytes())
                    i += 1
                    last_index = quart * i
                residu: int = 0
                residu = (file_size) % WORD_SIZE
                source_file.seek(last_index + 64)
                destination_file.write(
                np.bitwise_xor(np.frombuffer(source_file.read(
                    file_size - (
                        last_index + residu)
                    ), dtype=np.uint64), np_pass_phrase[0]).tobytes())
                if residu != 0:
                    i = 0
                    for data in chunker(input_file, residu):
                        destination_file.write(
                            (data ^ pass_phrase[i]).to_bytes(1, 'little'))
                        i += 1
    return None
