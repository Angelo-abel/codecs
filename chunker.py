def chunker(path: str):
    """Read 64 """
# if os.isfile(path):
    with open(path, 'rb') as file_handle:
        i: int = 0
        while True:
            data_chunk = file_handle.read(64)
            i += 64
            if not data_chunk:
                break
            yield data_chunk
