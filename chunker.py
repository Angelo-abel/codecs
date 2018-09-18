import os

def chunker(path: str):
    """Read 64 """
# if os.isfile(path):
    with open(path, 'rb') as file_handle:
        while True:
            data_chunk = file_handle.read(64)
            if not data_chunk:
                break
            yield data_chunk
