import os

from EncDecFixture import EncDecFixture
from codec import xor_inv

def test_xor_inv():
    fixture = EncDecFixture()
    fixture.setUp()
    if not os.path.isfile(fixture.temp_file):
        assert(False)
        return

    xor_inv.encode(fixture.temp_file, fixture.encode_file)
    xor_inv.decode(fixture.encode_file, fixture.decode_file)
    decode_file_content: bytes = b""
    with open(fixture.decode_file, 'rb') as file_decode_open:
        decode_file_content = file_decode_open.read()
    assert(decode_file_content == fixture.bytes_content)
    fixture.tearDown()
