import os

from codec import xor
from EncDecFixture import EncDecFixture


def test_xor():
    fixture = EncDecFixture()
    fixture.setUp()
    if not os.path.isfile(fixture.temp_file):
        assert(False)
        return
    xor.encode(fixture.temp_file, fixture.encode_file)
    xor.decode(fixture.encode_file, fixture.decode_file)

    decode_file_content: bytes = b""
    with open(fixture.decode_file, 'rb') as decode_file_open:
        decode_file_open = decode_file_open.read()
    assert(decode_file_open == fixture.bytes_content)
    fixture.tearDown()
