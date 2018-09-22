def chunker(path: str, size: int = 64)->None:
    """Read 64 """
# if os.isfile(path):
    with open(path, 'rb') as file_handle:
        while True:
            data_chunk = file_handle.read(size)
            if not data_chunk:
                break
            yield data_chunk
