def chunker(path_file: str, position: int = 0)->None:
    with open(path_file, 'rb') as source_file:
        source_file.seek(int(-position), 2)
        return source_file.read()
