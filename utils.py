from os import stat


def getFileSize(input_file_name: str)->int:
    return stat(input_file_name).st_size


def storeFile(file_name: str, line: bytes)->None:
    with open(file_name, 'wb') as file_handle:
            file_handle.write(line)
    return None
