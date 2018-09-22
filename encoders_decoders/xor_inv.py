from chunker import chunker

def encode(input_path: str, ouptut_filename: str)->None:
    encode_str: bytes = b""
    status: bool = True
    for chunk in chunker(input_path):
        for data in chunk:
            if status:
                encode_str += (data ^ 0x65).to_bytes(1, 'little')
            else:
                encode_str += (data ^ 0xFF).to_bytes(1, 'little')
            status = not status
    with open(ouptut_filename, 'wb') as open_file:
        open_file.write(encode_str)


def decode(input_path: str, ouptut_filename: str)->None:
    encode(input_path, ouptut_filename)
