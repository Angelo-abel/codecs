from chunker import chunker
from utils import *
from progressbar import progress
from metadata import *


def encode(input_file: str, output_file: str, validity: int = 0, bar: bool = False)->None:
    # encode_str: bytes = b""
    status: bool = True
    # file_size: int = getFileSize(input_file)
    # update_progress: int = int(0.25 * file_size)
    # update_step: int = update_progress
    # x: int  = 0
    with open(output_file, 'wb') as handle_file:
        if validity == 0:
            handle_file.write(metaDataGenerate())
            # encode_str += metaDataGenerate()
        else:
            handle_file.write(metaDataGenerate(validity))
            # encode_str += metaDataGenerate(validity)
        for chunk in chunker(input_file):
            for data in chunk:
                if status:
                    handle_file.write((data ^ 0x65).to_bytes(1, 'little'))
                    # encode_str += (data ^ 0x65).to_bytes(1, 'little')
                else:
                    handle_file.write((data ^ 0xFF).to_bytes(1, 'little'))
                    # encode_str += (data ^ 0xFF).to_bytes(1, 'little')
                status = not status
        #         if bar:
        #             x += 1
        #             if x == update_progress:
        #                 progress(x, file_size, "Encode")
        #                 update_progress += update_step
        # print()
    # storeFile(output_file, encode_str)
    return None


def decode(input_file: str, output_file: str, bar: bool = False)->None:
    if metaDataVerify(input_file):
        status: bool = True
        # file_size: int = getFileSize(input_file)
        # x: int = 0
        i: int = 0
        # update_progress: int = int(0.25 * file_size)
        # update_step: int = update_progress
        # decode_str: bytes = b""
        with open(output_file, 'wb') as handle_file:
            for chunk in chunker(input_file):
                for data in chunk:
                    if i > 64:
                        if status:
                            handle_file.write(
                                (data ^ 0x65).to_bytes(1, 'little'))
                            # decode_str += (data ^ 0x65).to_bytes(1, 'little')
                        else:
                            handle_file.write(
                                (data ^ 0xFF).to_bytes(1, 'little'))
                            # decode_str += (data ^ 0xFF).to_bytes(1, 'little')
                        status = not status
                    else:
                        i += 1
            #         if bar:
            #             x += 1
            #             if x == update_progress:
            #                 progress(x, file_size, 'Decode')
            #                 update_progress += update_step
            # print()
            # storeFile(output_file, decode_str)
    return None
