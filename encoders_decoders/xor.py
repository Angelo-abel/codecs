from chunker import chunker
from utils import *
from progressbar import progress
from metadata import *

"""0x65 = 'e' is the mask """

def encode(input_file: str, output_file: str, validity: int = 0)->None:
    file_size: int = getFileSize(input_file)
    x: int  = 0
    update_progress: int = int(0.1 * file_size)
    update_step: int = update_progress
    encode_str: bytes = b""
    if validity == 0:
        encode_str += metaDataGenerate()
    else:
        encode_str += metaDataGenerate(validity)
    for chunk in chunker(input_file):
        for data in chunk:
            encode_str += (data ^ 0x65).to_bytes(1, 'little')
            x += 1
            if x == update_progress:
                progress(x, file_size, "Encode")
                update_progress += update_step
    print()
    storeFile(output_file, encode_str)
    return None


def decode(input_file: str, output_file: str)->None:
    if metaDataVerify(input_file):
        file_size: int = getFileSize(input_file)
        x: int = 0
        i: int = 0
        update_progress: int = int(0.1 * file_size)
        update_step: int = update_progress
        decode_str: bytes = b""
        for chunk in chunker(input_file):
            for data in chunk:
                if i > 64:
                    decode_str += (data ^ 0x65).to_bytes(1, 'little')
                else:
                    i += 1
                x += 1
                if x == update_progress:
                    progress(x, file_size, 'Decode')
                    update_progress += update_step
        print()
        storeFile(output_file, decode_str)
    return None
