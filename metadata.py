from datetime import datetime
from base64 import b64encode
from base64 import b64decode
from random import randint
from UserException import NotEncodedError, ExpiredError

ORGANISATION: str = "ceceonat"
FORMAT_TIME: str ='%d-%m-%Y%H:%M:%S'


def metaDataGenerate(validity_time:int=0):
    mask = randint(100, 255)
    meta_data_encode = b"" + str(mask).encode('utf8')
    meta_data: bytes = b""
    current_time = datetime.now()
    if validity_time != 0:
        end_time = datetime.fromtimestamp(
            current_time.timestamp()+validity_time).strftime(FORMAT_TIME)
        meta_data = b64encode("{}{}E{}".format(
            ORGANISATION, current_time.strftime(
                FORMAT_TIME), end_time).encode('utf8'))
    else:
        meta_data = b64encode(
            ORGANISATION.encode('utf8') + datetime.now(
                ).strftime(FORMAT_TIME).encode('utf8'))
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
    date_exp: str = ''
    if ORGANISATION in meta_data_decode:
        data_encode = meta_data_decode.split('ceceonat')[1]
        if 'E' in data_encode:
            date_encode, date_exp = data_encode.split('E')
        else:
            date_encode = data_encode
        if datetime.strptime(date_encode, FORMAT_TIME).strftime(FORMAT_TIME) <= datetime.now().strftime(FORMAT_TIME):
            if date_exp != '' :
                if datetime.strptime(date_exp, FORMAT_TIME).strftime(FORMAT_TIME) >= datetime.now().strftime(FORMAT_TIME):
                    return True
                else:
                    raise ExpiredError
            return True
        else:
            raise NotEncodedError
    else:
        raise NotEncodedError
