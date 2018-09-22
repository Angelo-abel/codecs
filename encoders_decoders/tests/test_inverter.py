import os

from codec import inv 
from EncDecFixture import EncDecFixture


def test_inv():
    fixture = EncDecFixture()
    fixture.setUp()
    if not os.path.isfile(fixture.temp_file):
        assert(False)
        return
    inv.encode(fixture.temp_file, fixture.encode_file)
    inv.decode(fixture.encode_file, fixture.decode_file)
    decode_file_content: bytes = b""
    with open(fixture.decode_file, 'rb') as file_decode_open:
        decode_file_content = file_decode_open.read()
    assert(decode_file_content == fixture.bytes_content)
    fixture.tearDown()
