def extend_bytes(byte_str, length):
    if len(byte_str) >= length:
        return byte_str[:length]
    else:
        return byte_str + ((b' ') * (length - len(byte_str)))

def clean_output(out):
    if len(out) == 0:
        return out

    new_out = out.replace(b'\r\n', b'\n')
    return new_out


def get_file_name(path):
    file_name = path.split('/')[-1]
    file_name = file_name.split('.')[0]
    return file_name