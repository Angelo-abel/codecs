from datetime import datetime
from base64 import b64encode
from base64 import b64decode
from random import randint
from UserException import NotEncodedError


def metaDataGenerate():
    mask = randint(100, 255)
    meta_data_encode = b"" + str(mask).encode('utf8')
    meta_data: bytes = b64encode(
        b"ceceonat " + datetime.now(
            ).strftime('%d-%m-%Y %H:%M:%S').encode('utf8'))
    while len(meta_data) < 62:
        meta_data += b"="
    for data in meta_data:
        meta_data_encode += (data ^ mask).to_bytes(1, 'little')
    return meta_data_encode


def metaDataVerify(file_encoded: str)->bool:
    meta_data_encode = b""
    mask: str = ""
    with open(file_encoded, 'rb') as open_file_read:
        meta_data_encode = open_file_read.read(64)
    for i in range(3):
        mask += chr(meta_data_encode[i])

    # Decode meta data
    meta_data: bytes = b""
    for i in range(3, 64, 1):
        try:
            meta_data += (
                meta_data_encode[i] ^ int(mask)).to_bytes(1, 'little')
        except:
            raise NotEncodedError

    meta_data_decode = b64decode(meta_data).decode('utf8')
    date_encode: str = ''
    format_date: str = '%d-%m-%Y %H:%M:%S'
    if 'ceceonat' in meta_data_decode:
        date_encode = meta_data_decode.split('ceceonat')[1]
        if datetime.strptime(date_encode[1:], format_date).strftime(format_date) <= datetime.now().strftime(format_date):
            return True
        else:
            raise NotEncodedError
    else:
        raise NotEncodedError
