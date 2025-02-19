from datetime import date
import base64
import os
from constant import ENCRYPT_DIR, DECRYPT_DIR


class FileCRUD:
    @staticmethod
    def is_dir_exist(dir):
        if os.path.exists(dir) is False:
            os.mkdir(dir)

    @staticmethod
    def read_file(file_path):
        with open(file_path, "rb") as file:
            return file.read()

    @staticmethod
    def write_file(file_path, data):
        with open(file_path, "wb") as file:
            file.write(data)
            return FileCRUD.path_basename(file_path)

    @staticmethod
    def path_basename(file_path):
        return os.path.basename(file_path)

    @staticmethod
    def new_key_filename(type_method):
        type_key = ""

        if type_method.startswith(("AES", "receiver-RSA", "private-RSA")):
            type_key = type_method

        return f"key_{type_key}_{str(date.today())}.pem"

    @staticmethod
    def path_encrypt_file(file_path):
        basename = FileCRUD.path_basename(file_path)
        return os.path.join(ENCRYPT_DIR, f"{basename}.bin")

    @staticmethod
    def path_decrypt_file(file_path):
        basename = FileCRUD.path_basename(file_path)
        origin_name, ext = os.path.splitext(basename)
        return os.path.join(DECRYPT_DIR, f"enc_{origin_name}")

    @staticmethod
    def joint_byte_strings(strings):
        if len(strings) == 0:
            return b""

        response = []
        for str in strings:
            response.append(base64.b64decode(str))

        return base64.b64encode(bytearray(b"").join(response))

    @staticmethod
    def split_byte_strings(string, byte):
        if len(string) == 0:
            return (b"", b"")

        str_decode = base64.b64decode(string)
        first = base64.b64encode(str_decode[:byte])
        second = base64.b64encode(str_decode[byte:])
        return (first, second)
