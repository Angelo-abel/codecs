from chunker import chunker
from utils import *
from progressbar import progress
from metadata import *


def encode(input_file: str, output_file: str, pass_phrase: bytes,
    validity: int = 0)->None:
    encode_str: bytes = b""
    file_size: int = getFileSize(input_file)
    x: int  = 0
    index: int = 0
    update_progress: int = int(0.1 * file_size)
    update_step: int = update_progress
    if validity == 0:
        encode_str += metaDataGenerate()
    else:
        encode_str += metaDataGenerate(validity)
    for chunk in chunker(input_file):
        for data in chunk:
            encode_str += (data ^ pass_phrase[index]).to_bytes(1, 'little')
            if index < 127:
                index += 1
            else:
                index = 0
            x += 1
            if x == update_progress:
                progress(x, file_size, "Encode")
                update_progress += udapte_step
    print()
    storeFile(output_file, encode_str)
    return None


def decode(input_file: str, output_file: str, pass_phrase: bytes)->None:
    if metaDataVerify(input_file):
        decode_str: bytes = b""
        file_size: int = getFileSize(input_file)
        x: int  = 0
        index: int = 0
        i: int = 0
        update_progress: int = int(0.1 * file_size)
        update_step: int = update_progress
        for chunk in chunker(input_file):
            for data in chunk:
                if i > 64:
                    decode_str += (data ^ pass_phrase[index]).to_bytes(1, 'little')
                    if index < 127:
                        index += 1
                    else:
                        index = 0
                else:
                    i += 1
                x += 1
                if x == update_progress:
                    progress(x, file_size, "Decode")
                    update_progress += update_step
        print()
        storeFile(output_file, decode_str)
    return None
