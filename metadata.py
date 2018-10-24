from datetime import datetime
from base64 import b64encode
from base64 import b64decode
from UserException import NotEncodedError, ExpiredError
import numpy as np

ORGANISATION: str = "ceceonat"
FORMAT_TIME: str ='%d-%m-%Y%H:%M:%S'


def metaDataGenerate(validity_time:int=0)->bytes:
    meta_data: bytes = b""
    current_time = datetime.now()
    if validity_time != 0:
        meta_data = b64encode("{}{}E{}".format(
            ORGANISATION, current_time.strftime(
                FORMAT_TIME), datetime.fromtimestamp(
                current_time.timestamp(
                    ) + validity_time).strftime(FORMAT_TIME)).encode('utf8'))
    else:
        meta_data = b64encode(
            ORGANISATION.encode('utf8') + datetime.now(
                ).strftime(FORMAT_TIME).encode('utf8'))
    if len(meta_data) < 64:
        meta_data += (b"=" * (64-len(meta_data)))
    return np.invert(np.frombuffer(meta_data, dtype=np.uint64)).tobytes()


def metaDataVerify(file_encoded: str)->bool:
    meta_data_encode = b""
    with open(file_encoded, 'rb') as open_file_read:
        meta_data_encode = np.invert(np.frombuffer(
            open_file_read.read(64), dtype=np.uint64)).tobytes()
    # Decode meta data
    try:
        meta_data_decode = b64decode(meta_data_encode).decode('utf8')
    except:
        raise NotEncodedError
    date_encode: str = ''
    date_exp: str = ''
    if ORGANISATION in meta_data_decode:
        data_encode = meta_data_decode.split('ceceonat')[1]
        if 'E' in data_encode:
            date_encode, date_exp = data_encode.split('E')
        else:
            date_encode = data_encode
        if datetime.strptime(
            date_encode, FORMAT_TIME).strftime(
                FORMAT_TIME) <= datetime.now().strftime(FORMAT_TIME):
            if date_exp != '' :
                if datetime.strptime(
                  ate_exp, FORMAT_TIME).strftime(
                        FORMAT_TIME) >= datetime.now().strftime(FORMAT_TIME):
                    return True
                else:
                    raise ExpiredError
            return True
        else:
            raise NotEncodedError
    else:
        raise NotEncodedError
