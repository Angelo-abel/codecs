import os


class EncDecFixture:
    """docstring for EncDecFixture"""
    def __init__(self, temp_file: str = '/tmp/enc_dec.txt', encode_file: str='/tmp/encode_file', decode_file: str= '/tmp/decode_file'):
        self.temp_file = temp_file
        self.encode_file = encode_file
        self.decode_file = decode_file

    def setUp(self):
        self.content = """Lorem ipsum dolor sit amet, consectetur adipisicing
        elit, sed do eiusmod tempor incididunt ut labore et dolore magna
        aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
        laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor
        in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
        pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
        culpa qui officia deserunt mollit anim id est laborum."""
        with open(self.temp_file, 'w', encoding='utf8') as open_file_write:
            open_file_write.write(self.content)

        self.bytes_content: bytes =  b""
        with open(self.temp_file, 'rb') as open_file_read:
            self.bytes_content += open_file_read.read()

    def tearDown(self):
        os.remove(self.temp_file)
        os.remove(self.encode_file)
        os.remove(self.decode_file)
