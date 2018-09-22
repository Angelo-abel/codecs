import pytest
import os
from chunker import chunker


class chunkerFixture:
    """docstring for chunkerFixture"""
    def __init__(self, temp_file: str = '/tmp/chunker_file.txt'):
        self.temp_file = temp_file

    def setUp(self):
        self.content = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

        with open(self.temp_file, 'w', encoding='utf8') as open_file_write:
            open_file_write.write(self.content)

        self.bytes_content: bytes = b""
        with open(self.temp_file, 'rb') as open_file_read:
            self.bytes_content = open_file_read.read()

    def tearDown(self):
        os.remove(self.temp_file)
        pass


def chunker_n_bytes(size_chunk: int):
    fixture = chunkerFixture()
    fixture.setUp()
    if not os.path.isfile(fixture.temp_file):
        assert(False)
        return

    chunked_content: bytes = b""
    for chunk in chunker(fixture.temp_file, size_chunk):
        chunked_content += chunk

    assert(chunked_content == fixture.bytes_content)
    fixture.tearDown()


def test_chunker_1_byte():
    # Read 1 byte
    chunker_n_bytes(1)


def test_chunker_64_bytes():
    # Read 64 bytes(default)
    chunker_n_bytes(64)


def test_chunker_128_bytes():
    # Read 128 bytes
    chunker_n_bytes(128)


def test_chunker_256_bytes():
    # Read 256 bytes
    chunker_n_bytes(256)


def test_chunker_512_bytes():
    # Read 512 bytes
    chunker_n_bytes(512)


def test_chunker_1024_bytes():
    # Read 1024 bytes
    chunker_n_bytes(1024)
