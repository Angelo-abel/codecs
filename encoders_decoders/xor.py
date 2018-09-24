from chunker import chunker
from get_file_size import getFileSize
from progressbar import progress


def encode(input_path: str, output_filename: str, label:str="Encoding")->None:
    file_size: int = getFileSize(input_path)
    x: int  = 0
    encode_str: bytes = b""
    for chunk in chunker(input_path):
        for data in chunk:
            encode_str += (data ^ 0x65).to_bytes(1, 'little')
            x += 1
            progress(x, file_size, label)
    print()
    with open(output_filename, 'wb') as oepn_file:
        oepn_file.write(encode_str)
    return None


def decode(input_path: str, output_filename: str)->None:
    encode(input_path, output_filename, label="Decoding")
    return None
