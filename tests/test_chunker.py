import pytest
import os
from chunker import chunker


TMP_FILE: str = "/tmp/temp_file.txt"


@pytest.fixture(params=[TMP_FILE])
def setUp(request):
    param = request.param
    content = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non roident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

    with open(param, 'w', encoding='utf8') as temp_file_create:
        temp_file_create.write(content)

    content_file_bytes: bytes = b""
    with open(param, 'rb') as temp_file_read:
        content_file_bytes = temp_file_read.read()
        yield content_file_bytes
    print("EXECUTION DU TEARDOW")
    if os.path.isfile(param):
        os.remove(param)


def test_chunker(setUp):
    content_file_bytes: bytes = setUp
    if not os.path.isfile(TMP_FILE):
        assert False

    content: bytes = b""
    for chunk in chunker(TMP_FILE):
        content += chunk
    assert(content == content_file_bytes)
