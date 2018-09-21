from chunker import chunker

def encode(input_path: str, output_filename: str)->None:
    encode_str: bytes = b""
    for chunk in chunker(input_path):
        for data in chunk:
            encode_str += (data^0x65).to_bytes(1, 'little')
    with open(output_filename, 'wb') as oepn_file:
        oepn_file.write(encode_str)


def decode(input_path: str, output_filename: str)->None:
    encode(input_path, output_filename)
