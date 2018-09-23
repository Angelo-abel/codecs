from chunker import chunker
from get_file_size import getFileSize
from progressbar import progress


def encode(input_path: str, ouptut_filename: str)->None:
    encode_str: bytes = b""
    status: bool = True
    file_size: int = getFileSize(input_path)
    x: int  = 0
    for chunk in chunker(input_path):
        for data in chunk:
            if status:
                encode_str += (data ^ 0x65).to_bytes(1, 'little')
            else:
                encode_str += (data ^ 0xFF).to_bytes(1, 'little')
            status = not status
            x += 1
            progress(x, file_size)
    with open(ouptut_filename, 'wb') as open_file:
        open_file.write(encode_str)
    print()
    return None


def decode(input_path: str, ouptut_filename: str)->None:
    encode(input_path, ouptut_filename)
    return None
