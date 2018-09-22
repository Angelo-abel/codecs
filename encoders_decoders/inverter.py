from chunker import chunker


def encode(input_file: str, output_file: str)->None:
    encode_str: bytes = b""
    for chunk in chunker(input_file):
        for data in chunk:
            encode_str += (data ^ 0xFF).to_bytes(1, 'little', signed=True)
    with open(output_file, 'wb') as file_handle:
        file_handle.write(encode_str)


def decode(input_file: str, output_file: str)->None:
    encode(input_file, output_file)
