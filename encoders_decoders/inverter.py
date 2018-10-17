from chunker import chunker
# from utils import *
from progressbar import progress
from metadata import *

def encode(input_file: str, output_file: str, validity: int = 0, bar: bool = False)->None:
    # file_size: int = getFileSize(input_file)
    # x: int  = 0
    # update_progress: int = int(0.25 * file_size)
    # update_step: int = update_progress
    # encode_str: bytes = b""
    with open(output_file, 'wb') as destination_file:
        if validity == 0:
            destination_file.write(metaDataGenerate())
        else:
            destination_file.write(metaDataGenerate(validity))
        for chunk in chunker(input_file):
            for data in chunk:
                destination_file.write((data ^ 0xFF).to_bytes(1, 'little'))
                # if bar:
                #    x += 1
                #    if x == update_progress:
                #        progress(x, file_size, "Encode")
                #        update_progress += update_step
        # print()
    # storeFile(output_file, encode_str)
    return None

def decode(input_file: str, output_file: str, bar: bool = False)->None:
    if metaDataVerify(input_file):
        # file_size: int = getFileSize(input_file)
        # x: int = 0
        i: int = 0
        # update_progress: int = int(0.25 * file_size)
        # update_step: int = update_progress
        # decode_str: bytes = b""
        with open(output_file, 'wb') as destination_file:
            for chunk in chunker(input_file):
                for data in chunk:
                    if i > 64:
                        destination_file.write(
                            (data ^ 0xFF).to_bytes(1, 'little'))
                    else:
                        i += 1
                    # if bar:
                    #     x += 1
                    #     if x == update_progress:
                    #         progress(x, file_size, 'Decode')
                    #         update_progress += update_step
            # print()
        # storeFile(output_file, decode_str)
    return None
