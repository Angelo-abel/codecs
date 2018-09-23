from chunker import chunker
from get_file_size import getFileSize
from progressbar import progress


def encode(input_file: str, output_file: str)->None:
    file_size: int = getFileSize(input_file)
    x: int  = 0
    encode_str: bytes = b""
    for chunk in chunker(input_file):
        for data in chunk:
            encode_str += (data ^ 0xFF).to_bytes(1, 'little')
            x += 1
            progress(x, file_size)
    with open(output_file, 'wb') as file_handle:
        file_handle.write(encode_str)
    print()
    return None

def decode(input_file: str, output_file: str)->None:
    encode(input_file, output_file)
    return None
