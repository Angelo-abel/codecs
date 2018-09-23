from os import stat

def getFileSize(input_file_name: str)->int:
    return stat(input_file_name).st_size
